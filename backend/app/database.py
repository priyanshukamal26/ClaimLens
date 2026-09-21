"""
ClaimLens Nexus — Database Connections

Local dev: SQLite for application data, DuckDB (read-only) for analytics.
Production: DynamoDB replaces SQLite; DuckDB stays as the analytics layer.
"""

import sqlite3
import duckdb
from contextlib import contextmanager
from pathlib import Path

from app.config import SQLITE_DB_PATH, DUCKDB_PATH


# ============================================================
# SQLite — Application Data (policies, claims, decisions, etc.)
# ============================================================

def get_sqlite_connection() -> sqlite3.Connection:
    """Get a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def sqlite_session():
    """Context manager for SQLite transactions."""
    conn = get_sqlite_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_sqlite():
    """Initialize SQLite schema for application data."""
    with sqlite_session() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS policies (
                policy_id TEXT PRIMARY KEY,
                policyholder_name TEXT NOT NULL,
                state TEXT NOT NULL,
                line_of_business TEXT NOT NULL,
                insurer TEXT NOT NULL,
                premium_amount REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Active'
            );

            CREATE TABLE IF NOT EXISTS claims (
                claim_id TEXT PRIMARY KEY,
                policy_id TEXT NOT NULL,
                claim_amount REAL NOT NULL,
                claim_date TEXT NOT NULL,
                settlement_amount REAL,
                settlement_date TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                hospital_id TEXT,
                garage_id TEXT,
                agent_id TEXT,
                claim_type TEXT NOT NULL,
                fraud_flag INTEGER NOT NULL DEFAULT 0,
                anomaly_score REAL DEFAULT 0.0,
                anomaly_layers TEXT DEFAULT '{}',
                FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
            );

            CREATE TABLE IF NOT EXISTS hospitals (
                hospital_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                tpa_network TEXT,
                bed_count INTEGER
            );

            CREATE TABLE IF NOT EXISTS garages (
                garage_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                service_type TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                region TEXT NOT NULL,
                commission_rate REAL NOT NULL,
                active_policies_count INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                claim_id TEXT NOT NULL,
                insight_type TEXT NOT NULL,
                decision_type TEXT NOT NULL,
                decided_by TEXT NOT NULL,
                decided_at TEXT NOT NULL,
                rationale TEXT,
                FOREIGN KEY (claim_id) REFERENCES claims(claim_id)
            );

            CREATE INDEX IF NOT EXISTS idx_claims_policy ON claims(policy_id);
            CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);
            CREATE INDEX IF NOT EXISTS idx_claims_date ON claims(claim_date);
            CREATE INDEX IF NOT EXISTS idx_claims_anomaly ON claims(anomaly_score DESC);
            CREATE INDEX IF NOT EXISTS idx_decisions_claim ON decisions(claim_id);
            CREATE INDEX IF NOT EXISTS idx_policies_state ON policies(state);
            CREATE INDEX IF NOT EXISTS idx_policies_lob ON policies(line_of_business);
        """)


# ============================================================
# DuckDB — Read-Only Analytics Layer (per ADR-002)
# ============================================================
# Security: read-only, external access disabled per DuckDB security guidance.

_duckdb_conn = None
_duckdb_readonly = False


def get_duckdb_connection() -> duckdb.DuckDBPyConnection:
    """
    Get a persistent DuckDB connection for the analytics layer.

    Per ADR-002 and TECH_STACK.md:
    - After data loading, connection is read-only with external access disabled
    - SQL queries are additionally guarded by the sqlglot allowlist (guard.py)
    """
    global _duckdb_conn
    if _duckdb_conn is None:
        _duckdb_conn = duckdb.connect(str(DUCKDB_PATH), read_only=_duckdb_readonly)
        if _duckdb_readonly:
            # Security hardening: disable external access on the read-only connection
            _duckdb_conn.execute("SET enable_external_access = false")
    return _duckdb_conn


def init_duckdb_from_sqlite():
    """
    Load data from SQLite into DuckDB for the analytics layer.
    Called after synthetic data generation or data updates.

    External access must be enabled during this step (SQLite extension needs it).
    After loading, connection is closed and reopened read-only with external access disabled.
    """
    global _duckdb_conn, _duckdb_readonly

    # Close any existing connection
    if _duckdb_conn is not None:
        _duckdb_conn.close()
        _duckdb_conn = None

    # Open writable connection with external access enabled for data loading
    _duckdb_readonly = False
    loader_conn = duckdb.connect(str(DUCKDB_PATH), read_only=False)

    # Attach SQLite as a source and copy tables
    sqlite_path_str = str(SQLITE_DB_PATH).replace("\\", "/")
    loader_conn.execute(f"ATTACH '{sqlite_path_str}' AS sqlite_source (TYPE sqlite, READ_ONLY)")

    tables = ["policies", "claims", "hospitals", "garages", "agents", "decisions"]
    for table in tables:
        loader_conn.execute(f"DROP TABLE IF EXISTS {table}")
        loader_conn.execute(f"CREATE TABLE {table} AS SELECT * FROM sqlite_source.{table}")

    loader_conn.execute("DETACH sqlite_source")
    loader_conn.close()

    # Reopen as read-only with external access disabled (security hardening)
    _duckdb_readonly = True
    _duckdb_conn = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    _duckdb_conn.execute("SET enable_external_access = false")


def execute_analytics_query(sql: str, params: list = None) -> list[dict]:
    """
    Execute a read-only query against the DuckDB analytics layer.
    This is used by the Ask ClaimLens agent chain AFTER the SQL guard validates the query.
    """
    conn = get_duckdb_connection()
    if params:
        result = conn.execute(sql, params)
    else:
        result = conn.execute(sql)

    columns = [desc[0] for desc in result.description]
    rows = result.fetchall()
    return [dict(zip(columns, row)) for row in rows]
