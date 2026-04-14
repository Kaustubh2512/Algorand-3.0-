# routes/monitor.py
from fastapi import APIRouter, HTTPException
from schemas import StartMonitorRequest
from database import monitor_jobs_collection, alerts_collection
from models import new_monitor_job_doc

router = APIRouter()

@router.post("/monitor/start")
async def start_monitoring(req: StartMonitorRequest):
    """Register a contract address for 24/7 anomaly monitoring."""

    # Check if already monitoring this app for this wallet
    existing = await monitor_jobs_collection.find_one({
        "app_id":         req.app_id,
        "wallet_address": req.wallet_address,
        "is_active":      True
    })

    if existing:
        return {
            "job_id":  existing["_id"],
            "message": "Already monitoring this contract",
            "is_active": True
        }

    doc = new_monitor_job_doc(
        wallet_address=req.wallet_address,
        app_id=req.app_id,
        account_address=req.account_address,
        telegram_chat_id=req.telegram_chat_id
    )

    await monitor_jobs_collection.insert_one(doc)

    return {
        "job_id":  doc["_id"],
        "message": "Monitoring started successfully",
        "is_active": True
    }


@router.post("/monitor/stop/{job_id}")
async def stop_monitoring(job_id: str):
    """Stop a monitoring job."""
    result = await monitor_jobs_collection.update_one(
        {"_id": job_id},
        {"$set": {"is_active": False}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Monitor job not found")

    return {"message": "Monitoring stopped", "job_id": job_id}


@router.get("/monitor/{app_id}/alerts")
async def get_alerts(app_id: int, wallet_address: str):
    """Get the latest anomaly alerts for a monitored contract."""

    job = await monitor_jobs_collection.find_one({
        "app_id":         app_id,
        "wallet_address": wallet_address
    })

    if not job:
        raise HTTPException(status_code=404, detail="No monitor job found for this app_id and wallet")

    cursor = alerts_collection.find(
        {"monitor_job_id": job["_id"]}
    ).sort("created_at", -1).limit(20)

    alert_list = []
    async for a in cursor:
        alert_list.append({
            "id":            a["_id"],
            "severity":      a["severity"],
            "description":   a["description"],
            "anomaly_score": a["anomaly_score"],
            "txn_id":        a.get("txn_id"),
            "is_read":       a["is_read"],
            "timestamp":     a["created_at"].isoformat()
        })

    # Mark alerts as read
    await alerts_collection.update_many(
        {"monitor_job_id": job["_id"], "is_read": False},
        {"$set": {"is_read": True}}
    )

    return {
        "job_id":    job["_id"],
        "is_active": job["is_active"],
        "app_id":    app_id,
        "alerts":    alert_list
    }


@router.get("/monitor/jobs/{wallet_address}")
async def get_monitor_jobs(wallet_address: str):
    """Get all monitor jobs for a wallet."""
    cursor = monitor_jobs_collection.find({"wallet_address": wallet_address})

    jobs = []
    async for job in cursor:
        jobs.append({
            "job_id":          job["_id"],
            "app_id":          job["app_id"],
            "account_address": job["account_address"],
            "is_active":       job["is_active"],
            "created_at":      job["created_at"].isoformat()
        })

    return jobs
