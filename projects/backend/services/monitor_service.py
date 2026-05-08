# services/monitor_service.py
import os
import uuid
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
try:
    from utils.blockchain_indexer import fetch_contract_transactions
    from utils.email_service import send_alert_email
    from ml_models.anomaly import get_monitor
except ImportError:
    pass
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL    = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "algoshield")

# Use sync PyMongo here (not Motor) because APScheduler runs in a thread, not async
_sync_client = MongoClient(MONGODB_URL)
_sync_db     = _sync_client[MONGODB_DB_NAME]

scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            run_monitoring_cycle,
            trigger='interval',
            seconds=30,
            id='monitor_cycle',
            replace_existing=True
        )
        scheduler.start()
        print("✅ AlgoShield monitoring scheduler started (every 30s)")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Scheduler stopped")

def run_monitoring_cycle():
    """
    Called every 30 seconds by APScheduler.
    Fetches new transactions for each active monitor job,
    runs anomaly detection, saves alerts, sends Email messages.
    """

    # APScheduler runs in a separate thread. We must run async code using asyncio
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    monitor_jobs = _sync_db["monitor_jobs"]
    alerts       = _sync_db["alerts"]

    active_jobs = list(monitor_jobs.find({"is_active": True}))

    for job in active_jobs:
        job_id = job["_id"]

        try:
            # 1. Fetch new transactions from Algorand Indexer
            new_txns = loop.run_until_complete(fetch_contract_transactions(
                contract_address=job["account_address"],
                min_round=job.get("last_round", 0)
            ))

            if not new_txns:
                continue

            # 2. Update the last seen round based on highest confirmed-round in new txns
            highest_round = job.get("last_round", 0)
            for txn in new_txns:
                rnd = txn.get("confirmed-round", 0)
                if rnd > highest_round:
                    highest_round = rnd

            monitor_jobs.update_one(
                {"_id": job_id},
                {"$set": {"last_round": highest_round + 1}} # next time fetch from next round
            )

            # 3. Feed transactions to the Isolation Forest model
            # Assuming get_monitor still exists locally or we should adapt it.
            # wait, the original code had: from monitor import get_monitor
            ai_monitor = get_monitor(str(job["app_id"]))
            ai_monitor.add_transactions(new_txns)

            # 4. Check each new transaction for anomalies
            for txn in new_txns:
                result = ai_monitor.check_transaction(txn)

                if result.get("is_anomaly"):
                    # 5. Save alert to MongoDB
                    alert_doc = {
                        "_id":            str(uuid.uuid4()),
                        "monitor_job_id": job_id,
                        "app_id":         job["app_id"],
                        "txn_id":         txn.get("id"),
                        "anomaly_score":  result["anomaly_score"],
                        "severity":       result["severity"],
                        "description":    result["description"],
                        "is_read":        False,
                        "created_at":     datetime.utcnow()
                    }
                    alerts.insert_one(alert_doc)

                    print(f"🚨 Anomaly detected — App {job['app_id']} | {result['severity']} | {result['description']}")

                    # 6. Send Email notification if configured
                    if job.get("alert_email"):
                        send_alert_email(
                            to_email=job["alert_email"],
                            contract_address=job["account_address"],
                            txn_id=txn.get("id", "Unknown"),
                            txn_type=txn.get("tx-type", "Unknown"),
                            risk_level=result["severity"],
                            label=result["description"]
                        )

        except Exception as e:
            print(f"Error in monitor job {job_id}: {e}")

