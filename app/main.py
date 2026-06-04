from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.middleware import LoggingMiddleware
from app.stream_consumer import start_event_consumer
from app.seed_data import seed_database

from app.health import router as health_router
from app.ingestion import router as ingestion_router
from app.metrics import router as metrics_router
from app.funnel import router as funnel_router
from app.heatmap import router as heatmap_router
from app.anomalies import router as anomalies_router


# --------------------------------------------------
# CREATE DATABASE TABLES
# --------------------------------------------------
Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# STARTUP / SHUTDOWN
# --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Auto-seed database on first startup
    seed_database()

    # Start background consumer
    start_event_consumer()

    yield


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------
app = FastAPI(
    title="Store Intelligence API",
    version="1.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
app.add_middleware(LoggingMiddleware)


# --------------------------------------------------
# ROUTERS
# --------------------------------------------------
app.include_router(health_router)
app.include_router(ingestion_router)
app.include_router(metrics_router)
app.include_router(funnel_router)
app.include_router(heatmap_router)
app.include_router(anomalies_router)


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Store Intelligence API is running"
    }


# --------------------------------------------------
# MANUAL SEED ENDPOINT
# --------------------------------------------------
@app.post("/seed")
def seed():
    seed_database()
    return {
        "message": "Database seeded successfully"
    }