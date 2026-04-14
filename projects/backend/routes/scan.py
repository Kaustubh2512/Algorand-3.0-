# routes/scan.py
import hashlib
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Header, Depends
from database import scans_collection
from models import new_scan_doc

router = APIRouter()

VALID_API_KEYS = {"demo-key-123", "hackathon-key-456"}

async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key and x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.post("/scan")
async def scan_contract(
    wallet_address: str = Form(...),
    file: UploadFile = File(None),
    app_id: int = Form(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Accepts either:
    - A .teal or .py file upload
    - An Algorand App ID (fetches real TEAL from mainnet)

    Returns the full security scan result.
    """
    # Step 1: Get the contract code
    if file:
        raw = await file.read()
        try:
            contract_code = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File must be a UTF-8 text file (.teal or .py)")
        contract_filename = file.filename

    elif app_id:
        try:
            from algorand_fetcher import fetch_contract_by_app_id
            fetched = fetch_contract_by_app_id(app_id, use_mainnet=True)
            contract_code = fetched["approval_program"]
            contract_filename = None
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Could not fetch App ID {app_id}: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Provide either a file upload or an app_id")

    if not contract_code or not contract_code.strip():
        raise HTTPException(status_code=400, detail="Contract code is empty")

    # Step 2: Run AI security scan
    try:
        from scanner import scan_contract as ai_scan
        scan_result = ai_scan(contract_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI scan failed: {str(e)}")

    # Step 3: Save result to MongoDB
    contract_hash = hashlib.sha256(contract_code.encode()).hexdigest()

    doc = new_scan_doc(
        wallet_address=wallet_address,
        contract_code=contract_code,
        contract_hash=contract_hash,
        score=scan_result["score"],
        risk_level=scan_result["risk_level"],
        vulnerabilities=scan_result.get("vulnerabilities", []),
        summary=scan_result.get("summary", ""),
        app_id=app_id,
        contract_filename=contract_filename
    )

    await scans_collection.insert_one(doc)

    return {
        "scan_id":        doc["_id"],
        "score":          doc["score"],
        "risk_level":     doc["risk_level"],
        "vulnerabilities": doc["vulnerabilities"],
        "summary":        doc["summary"],
        "contract_code":  contract_code,
        "contract_hash":  contract_hash
    }


@router.get("/scans/{wallet_address}")
async def get_scan_history(wallet_address: str):
    """Return last 10 scans for this wallet address."""
    cursor = scans_collection.find(
        {"wallet_address": wallet_address},
        # Exclude the full contract_code from the list view (keep it small)
        {"contract_code": 0}
    ).sort("created_at", -1).limit(10)

    results = []
    async for doc in cursor:
        results.append({
            "scan_id":    doc["_id"],
            "score":      doc["score"],
            "risk_level": doc["risk_level"],
            "app_id":     doc.get("app_id"),
            "filename":   doc.get("contract_filename"),
            "created_at": doc["created_at"].isoformat()
        })

    return results


@router.get("/scan/{scan_id}")
async def get_scan(scan_id: str):
    """Get a single scan result by its ID."""
    doc = await scans_collection.find_one({"_id": scan_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scan not found")

    doc["scan_id"] = doc.pop("_id")
    doc["created_at"] = doc["created_at"].isoformat()
    return doc
