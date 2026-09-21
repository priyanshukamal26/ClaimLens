"""
ClaimLens Nexus — FastAPI Application Entry Point

Per ARCHITECTURE.md: FastAPI on Lambda, serving the React SPA's API needs.
Local dev: runs via uvicorn. Production: deployed on AWS Lambda behind API Gateway.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS, DEBUG
from app.database import init_sqlite, init_duckdb_from_sqlite


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize databases and load data on startup."""
    # Initialize SQLite schema
    init_sqlite()

    # Check if data exists, if not generate synthetic data
    from app.data.loader import ensure_data_loaded
    ensure_data_loaded()

    # Load data into DuckDB analytics layer
    init_duckdb_from_sqlite()

    # Run anomaly detection pipeline
    from app.detection.scorer import run_full_detection_pipeline
    run_full_detection_pipeline()

    # Reload DuckDB after anomaly scores are written
    init_duckdb_from_sqlite()

    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Insurance analytics platform — insights, never decisions.",
    lifespan=lifespan,
)

# CORS for local dev (React on :5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
from app.routers import trends, anomalies, ask, decisions, brief, external, health

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(trends.router, prefix="/api/trends", tags=["Trends"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["Anomalies"])
app.include_router(ask.router, prefix="/api", tags=["Ask ClaimLens"])
app.include_router(decisions.router, prefix="/api/decisions", tags=["Decisions"])
app.include_router(brief.router, prefix="/api/brief", tags=["Morning Brief"])
app.include_router(external.router, prefix="/api/external", tags=["External Data"])
