# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_indexes
from services.monitor_service import start_scheduler, shutdown_scheduler
from routes import scan, certificates, monitor, contracts

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await create_indexes()
        start_scheduler()
        print("AlgoShield AI backend started")
    except Exception as e:
        print(f"ERROR: Backend initialization failed (is MongoDB running?): {e}")
    yield
    # Shutdown
    try:
        shutdown_scheduler()
    except:
        pass
    print("AlgoShield backend stopped")

app = FastAPI(
    title="AlgoShield AI API",
    version="1.0.0",
    description="Algorand smart contract security platform",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router,         prefix="/api", tags=["Scan"])
app.include_router(certificates.router, prefix="/api", tags=["Certificates"])
app.include_router(monitor.router,      prefix="/api", tags=["Monitor"])
app.include_router(contracts.router,    prefix="/api", tags=["Contracts"])

@app.get("/health")
def health_check():
    return {"status": "AlgoShield AI is running", "version": "1.0.0"}
