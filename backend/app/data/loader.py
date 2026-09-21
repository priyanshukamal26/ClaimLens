"""
ClaimLens Nexus — Data Loader

Loads generated synthetic data into SQLite (application data store).
DuckDB loading is handled separately by database.init_duckdb_from_sqlite().
"""

import sqlite3
from app.config import SQLITE_DB_PATH
from app.database import sqlite_session


def ensure_data_loaded():
    """Check if data exists in SQLite; if not, generate and load it."""
    with sqlite_session() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM policies")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Data already loaded: {count} policies found. Skipping generation.")
            return

    print("No data found. Generating synthetic data...")
    from app.data.generator import SyntheticDataGenerator

    gen = SyntheticDataGenerator(seed=42)
    data = gen.generate_all()

    _load_into_sqlite(data)
    print("Synthetic data loaded into SQLite successfully.")


def _load_into_sqlite(data: dict):
    """Bulk insert generated data into SQLite."""
    with sqlite_session() as conn:
        # Hospitals
        conn.executemany(
            "INSERT OR REPLACE INTO hospitals VALUES (?, ?, ?, ?, ?, ?)",
            [(h["hospital_id"], h["name"], h["city"], h["state"],
              h["tpa_network"], h["bed_count"]) for h in data["hospitals"]]
        )

        # Garages
        conn.executemany(
            "INSERT OR REPLACE INTO garages VALUES (?, ?, ?, ?, ?)",
            [(g["garage_id"], g["name"], g["city"], g["state"],
              g["service_type"]) for g in data["garages"]]
        )

        # Agents
        conn.executemany(
            "INSERT OR REPLACE INTO agents VALUES (?, ?, ?, ?, ?)",
            [(a["agent_id"], a["name"], a["region"], a["commission_rate"],
              a["active_policies_count"]) for a in data["agents"]]
        )

        # Policies
        conn.executemany(
            "INSERT OR REPLACE INTO policies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(p["policy_id"], p["policyholder_name"], p["state"],
              p["line_of_business"], p["insurer"], p["premium_amount"],
              p["start_date"], p["end_date"], p["status"]) for p in data["policies"]]
        )

        # Claims
        conn.executemany(
            "INSERT OR REPLACE INTO claims VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(c["claim_id"], c["policy_id"], c["claim_amount"], c["claim_date"],
              c["settlement_amount"], c["settlement_date"], c["status"],
              c["hospital_id"], c["garage_id"], c["agent_id"], c["claim_type"],
              c["fraud_flag"], c["anomaly_score"], c["anomaly_layers"])
             for c in data["claims"]]
        )

        print(f"Loaded: {len(data['policies'])} policies, {len(data['claims'])} claims, "
              f"{len(data['hospitals'])} hospitals, {len(data['garages'])} garages, "
              f"{len(data['agents'])} agents")
