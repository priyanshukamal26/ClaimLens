"""
ClaimLens Nexus — Application Configuration

All secrets and model IDs are loaded from environment variables.
Per AI_ML.md: NEVER hardcode LLM model IDs. Confirm in-console each session.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

SQLITE_DB_PATH = DATA_DIR / "claimlens.db"
DUCKDB_PATH = DATA_DIR / "analytics.duckdb"

# --- LLM Configuration (ADR-003: 4-stage fallback chain) ---
# Per AI_ML.md: Do NOT hardcode model IDs from memory or docs.
# Confirm the live GA model ID in Google AI Studio / Groq console each session.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "")  # e.g. "llama-3.1-8b-instant" — confirm in console
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID", "")  # e.g. "gemini-3.1-flash" — confirm in console
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta"

# --- Rate Limit Awareness (per COST_PLAN.md) ---
# Groq free tier: ~30 req/min, ~1,000 req/day per model (varies)
# These are awareness constants, not enforced limits — the fallback chain handles exhaustion.
GROQ_RATE_LIMIT_RPM = 30
GROQ_RATE_LIMIT_RPD = 1000

# --- Application ---
APP_NAME = "ClaimLens Nexus"
APP_VERSION = "0.1.0"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# --- Synthetic Data ---
SYNTHETIC_POLICIES_COUNT = 5000
SYNTHETIC_CLAIMS_COUNT = 8000
SYNTHETIC_HOSPITALS_COUNT = 200
SYNTHETIC_GARAGES_COUNT = 150
SYNTHETIC_AGENTS_COUNT = 100

# --- Calibration (verified against IRDAI data, DATA.md) ---
# Non-life incurred claims ratio FY2024-25: 82.88%
CALIBRATION_CLAIMS_RATIO = 0.8288
# Claims settled by count: ~82%
CALIBRATION_SETTLEMENT_RATE = 0.82
