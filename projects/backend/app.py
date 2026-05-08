# backend/app.py
import uuid, hashlib, os, requests
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from utils.feature_extractor import extract_features_from_teal
from utils.feature_engineer import engineer_features
from ml_models.suggester import generate_suggestions
# Use ml_models instead of models to maintain directory fix
from ml_models.inference import predict
from database import scans_col, certificates_col, monitor_jobs_col, alerts_col, create_indexes

# ── APScheduler for monitoring
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
load_dotenv()

ca = certifi.where()
scheduler = BackgroundScheduler()
_sync_db = MongoClient(
    os.getenv("MONGODB_URL"), 
    tlsCAFile=ca, 
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000
)[os.getenv("MONGODB_DB_NAME", "algoshield")]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        await create_indexes()
        print("✅ MongoDB Indexes verified")
    except Exception as e:
        print(f"⚠️ Warning: Database initialization skipped or failed: {e}")

    try:
        from services.monitor_service import run_monitoring_cycle
        scheduler.add_job(run_monitoring_cycle, 'interval', seconds=30, id='monitor', replace_existing=True)
        scheduler.start()
        print("✅ Background Monitoring started")
    except Exception as e:
        print(f"⚠️ Warning: Scheduler failed to start: {e}")

    print("🚀 AlgoShield AI Backend is ready")
    yield
    # Shutdown logic
    scheduler.shutdown(wait=False)

app = FastAPI(title="AlgoShield AI", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.scan import router as scan_router
app.include_router(scan_router)


# ──────────────────────────────────────────────
# ROUTE 1 — Scan (expanded from original /analyze)
# ──────────────────────────────────────────────
@app.post("/analyze")
async def analyze_smart_contract(
    file: UploadFile = File(...),
    wallet_address: str = Form(default="anonymous")
):
    if not file.filename.endswith('.teal'):
        raise HTTPException(status_code=400, detail="Only .teal files are allowed")
    try:
        content = (await file.read()).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    try:
        # Step 1: Use the comprehensive scanner logic
        from scanner import scan_contract
        result = scan_contract(content)
        
        # Step 2: Map scanner results to match frontend expectations
        # The frontend expects 'score', 'risk_level', 'vulnerabilities', 'contract_code'
        vulnerabilities = result.get("suggestions", [])
        score = result.get("score", 50)
        risk_level = result.get("risk_level", "Risky")
        prediction_label = result.get("ml_label", "SUSPICIOUS") # Fallback from summary if needed
        
        # Step 3: Save to MongoDB for persistent history
        scan_id = str(uuid.uuid4())
        contract_hash = hashlib.sha256(content.encode()).hexdigest()

        doc = {
            "_id": scan_id,
            "wallet_address": wallet_address,
            "filename": file.filename,
            "contract_code": content,
            "contract_hash": contract_hash,
            "score": int(score),
            "risk_level": risk_level,
            "ml_label": result.get("label", "SUSPICIOUS"), # Correct key from Predictor
            "vulnerabilities": vulnerabilities,
            "summary": result.get("summary", ""),
            "created_at": datetime.utcnow()
        }
        await scans_col.insert_one(doc)

        # Step 4: Final response
        return {
            "scan_id": scan_id,
            "score": int(score),
            "risk_level": risk_level,
            "vulnerabilities": vulnerabilities,
            "contract_code": content,
            "contract_hash": contract_hash,
            "summary": result.get("summary", ""),
            "label": result.get("label", "SUSPICIOUS")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# ──────────────────────────────────────────────
# ROUTE 2 — Scan history for a wallet
# ──────────────────────────────────────────────
@app.get("/scans/{wallet_address}")
async def get_scans(wallet_address: str):
    cursor = scans_col.find(
        {"wallet_address": wallet_address},
        {"contract_code": 0}  # don't return full code in list
    ).sort("created_at", -1).limit(10)

    results = []
    async for doc in cursor:
        results.append({
            "scan_id":    doc["_id"],
            "filename":   doc.get("filename"),
            "score":      doc.get("score"),
            "risk_level": doc.get("risk_level"),
            "ml_label":   doc.get("ml_label"),
            "vuln_count": len(doc.get("vulnerabilities", [])),
            "created_at": doc["created_at"].isoformat()
        })
    return results

# ──────────────────────────────────────────────
# ROUTE 3 — Get single scan
# ──────────────────────────────────────────────
@app.get("/scan/{scan_id}")
async def get_scan(scan_id: str):
    doc = await scans_col.find_one({"_id": scan_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scan not found")
    doc["scan_id"] = doc.pop("_id")
    doc["created_at"] = doc["created_at"].isoformat()
    return doc

# ──────────────────────────────────────────────
# ROUTE 4 — Mint NFT Certificate
# ──────────────────────────────────────────────
class MintRequest(BaseModel):
    scan_id: str
    wallet_address: str

@app.post("/mint-certificate")
async def mint_certificate(req: MintRequest):
    scan = await scans_col.find_one({"_id": req.scan_id})
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan["score"] < 70:
        raise HTTPException(status_code=400, detail=f"Score must be 70+ to mint. Current: {scan['score']}")
    if scan["wallet_address"] != req.wallet_address:
        raise HTTPException(status_code=403, detail="Wallet address mismatch")

    existing = await certificates_col.find_one({"scan_id": req.scan_id})
    if existing:
        existing["cert_id"] = existing.pop("_id")
        existing["created_at"] = existing["created_at"].isoformat()
        return {**existing, "message": "Already minted"}

    try:
        from blockchain.nft_minter import mint_security_certificate
        mint_result = mint_security_certificate(
            recipient_address=req.wallet_address,
            app_id=0,
            security_score=scan["score"],
            scan_id=req.scan_id,
            contract_hash=scan["contract_hash"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Minting failed: {e}")

    cert_id = str(uuid.uuid4())
    doc = {
        "_id": cert_id,
        "scan_id": req.scan_id,
        "wallet_address": req.wallet_address,
        "asset_id": mint_result["asset_id"],
        "txn_id": mint_result["txn_id"],
        "explorer_url": mint_result["explorer_url"],
        "score": scan["score"],
        "filename": scan.get("filename"),
        "created_at": datetime.utcnow()
    }
    await certificates_col.insert_one(doc)
    return {"cert_id": cert_id, **mint_result, "minted_at": doc["created_at"].isoformat()}

# ──────────────────────────────────────────────
# ROUTE 5 — Get certificates for wallet
# ──────────────────────────────────────────────
@app.get("/certificates/{wallet_address}")
async def get_certificates(wallet_address: str):
    cursor = certificates_col.find({"wallet_address": wallet_address}).sort("created_at", -1)
    results = []
    async for doc in cursor:
        results.append({
            "cert_id":      doc["_id"],
            "scan_id":      doc["scan_id"],
            "asset_id":     doc["asset_id"],
            "txn_id":       doc["txn_id"],
            "explorer_url": doc["explorer_url"],
            "score":        doc["score"],
            "filename":     doc.get("filename"),
            "minted_at":    doc["created_at"].isoformat()
        })
    return results

# ──────────────────────────────────────────────
# ROUTE 6 — Start monitoring
# ──────────────────────────────────────────────
class MonitorRequest(BaseModel):
    wallet_address: str
    app_id: int
    account_address: str
    telegram_chat_id: Optional[str] = None
    alert_email: Optional[str] = None

@app.post("/monitor/start")
async def start_monitoring(req: MonitorRequest):
    existing = await monitor_jobs_col.find_one({
        "app_id": req.app_id,
        "wallet_address": req.wallet_address,
        "is_active": True
    })
    if existing:
        return {"job_id": existing["_id"], "message": "Already monitoring"}

    job_id = str(uuid.uuid4())
    await monitor_jobs_col.insert_one({
        "_id": job_id,
        "wallet_address": req.wallet_address,
        "app_id": req.app_id,
        "account_address": req.account_address,
        "telegram_chat_id": req.telegram_chat_id,
        "alert_email": req.alert_email,
        "is_active": True,
        "last_txn_id": None,
        "created_at": datetime.utcnow()
    })
    return {"job_id": job_id, "message": "Monitoring started"}

@app.post("/monitor/stop/{job_id}")
async def stop_monitoring(job_id: str):
    result = await monitor_jobs_col.update_one(
        {"_id": job_id},
        {"$set": {"is_active": False}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Monitor job not found")
    return {"message": "Monitoring stopped", "job_id": job_id}

# ──────────────────────────────────────────────
# ROUTE 7 — Get alerts
# ──────────────────────────────────────────────
@app.get("/monitor/{app_id}/alerts")
async def get_alerts(app_id: int, wallet_address: str):
    job = await monitor_jobs_col.find_one({"app_id": app_id, "wallet_address": wallet_address})
    if not job:
        raise HTTPException(status_code=404, detail="Monitor job not found")
    cursor = alerts_col.find({"monitor_job_id": job["_id"]}).sort("created_at", -1).limit(20)
    alert_list = []
    async for a in cursor:
        alert_list.append({
            "id": a["_id"], "severity": a["severity"],
            "description": a["description"], "anomaly_score": a["anomaly_score"],
            "txn_id": a.get("txn_id"), "timestamp": a["created_at"].isoformat()
        })
    return {"job_id": job["_id"], "is_active": job["is_active"], "alerts": alert_list}

# ──────────────────────────────────────────────
# ROUTE 8 — Health check
# ──────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "AlgoShield AI running", "version": "2.0.0"}

# ──────────────────────────────────────────────
# BACKGROUND MONITOR CYCLE (every 30s)
# ──────────────────────────────────────────────
def monitor_cycle():
    try:
        from blockchain.poller import poll_new_transactions
        from ml_models.anomaly import get_monitor
    except ImportError:
        return

    jobs = list(_sync_db["monitor_jobs"].find({"is_active": True}))
    for job in jobs:
        try:
            new_txns = poll_new_transactions(job["account_address"], job["app_id"], job.get("last_txn_id"))
            if not new_txns:
                continue
            _sync_db["monitor_jobs"].update_one({"_id": job["_id"]}, {"$set": {"last_txn_id": new_txns[0].get("id")}})
            mon = get_monitor(str(job["app_id"]))
            mon.add_transactions(new_txns)
            for txn in new_txns:
                result = mon.check_transaction(txn)
                if result.get("is_anomaly"):
                    alert_id = str(uuid.uuid4())
                    _sync_db["alerts"].insert_one({
                        "_id": alert_id, "monitor_job_id": job["_id"],
                        "app_id": job["app_id"], "txn_id": txn.get("id"),
                        "anomaly_score": result["anomaly_score"],
                        "severity": result["severity"], "description": result["description"],
                        "is_read": False, "created_at": datetime.utcnow()
                    })
                    if job.get("telegram_chat_id"):
                        _send_telegram(job["telegram_chat_id"], job["app_id"], result)
        except Exception as e:
            print(f"Monitor error job {job['_id']}: {e}")

def _send_telegram(chat_id, app_id, result):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        return
    emoji = {"Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🔵"}.get(result["severity"],"⚠️")
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={
        "chat_id": chat_id,
        "text": f"{emoji} *AlgoShield Alert*\nApp: `{app_id}`\nSeverity: *{result['severity']}*\n{result['description']}\n[View](https://allo.info/app/{app_id})",
        "parse_mode": "Markdown"
    }, timeout=5)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
