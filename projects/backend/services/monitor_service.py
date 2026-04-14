# services/monitor_service.py
import os
import uuid
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
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
    runs anomaly detection, saves alerts, sends Telegram messages.
    """
    try:
        from poller import poll_new_transactions
        from monitor import get_monitor
    except ImportError as e:
        print(f"Monitor cycle: module not ready yet ({e})")
        return

    monitor_jobs = _sync_db["monitor_jobs"]
    alerts       = _sync_db["alerts"]

    active_jobs = list(monitor_jobs.find({"is_active": True}))

    for job in active_jobs:
        job_id = job["_id"]

        try:
            # 1. Fetch new transactions from Algorand Indexer
            new_txns = poll_new_transactions(
                account_address=job["account_address"],
                app_id=job["app_id"],
                last_seen_txn_id=job.get("last_txn_id")
            )

            if not new_txns:
                continue

            # 2. Update the last seen transaction ID
            monitor_jobs.update_one(
                {"_id": job_id},
                {"$set": {"last_txn_id": new_txns[0].get("id")}}
            )

            # 3. Feed transactions to the Isolation Forest model
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

                    # 6. Send Telegram notification if configured
                    if job.get("telegram_chat_id"):
                        send_telegram_alert(
                            chat_id=job["telegram_chat_id"],
                            app_id=job["app_id"],
                            anomaly_result=result
                        )

        except Exception as e:
            print(f"Error in monitor job {job_id}: {e}")


def send_telegram_alert(chat_id: str, app_id: int, anomaly_result: dict):
    """
    Send a Telegram message when an anomaly is detected.
    Uses the Telegram Bot API directly (no library needed).
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("TELEGRAM_BOT_TOKEN not set — skipping alert")
        return

    severity_emoji = {
        "Critical": "🔴",
        "High":     "🟠",
        "Medium":   "🟡",
        "Low":      "🔵"
    }.get(anomaly_result.get("severity", ""), "⚠️")

    message = (
        f"{severity_emoji} *AlgoShield Security Alert*\n\n"
        f"App ID: `{app_id}`\n"
        f"Severity: *{anomaly_result.get('severity', 'Unknown')}*\n"
        f"Anomaly Score: `{anomaly_result.get('anomaly_score', 0)}`\n\n"
        f"📋 {anomaly_result.get('description', 'Suspicious activity detected')}\n\n"
        f"🔗 [View on Allo Explorer](https://allo.info/app/{app_id})\n"
        f"🛡️ Powered by AlgoShield AI"
    )

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                "chat_id":    chat_id,
                "text":       message,
                "parse_mode": "Markdown"
            },
            timeout=5
        )
        if response.status_code != 200:
            print(f"Telegram error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Telegram send failed: {e}")
