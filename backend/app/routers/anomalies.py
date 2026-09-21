"""
ClaimLens Nexus — Anomalies Router (FR-003)

Ranked review queue of flagged claims, with per-layer anomaly detail.
Every item is badged INSIGHT, never DECISION (ADR-004).
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.database import execute_analytics_query

router = APIRouter()


@router.get("/queue")
async def get_anomaly_queue(
    min_score: float = Query(0.2, description="Minimum anomaly score"),
    lob: Optional[str] = Query(None, description="Filter by line of business"),
    limit: int = Query(50, description="Max results"),
    offset: int = Query(0, description="Offset for pagination"),
):
    """
    Ranked review queue of flagged claims.

    Per ADR-004: every item here is an INSIGHT requiring human review.
    Items are never auto-decided — they route to the Decision Log.
    """
    where_clauses = ["c.anomaly_score >= " + str(min_score)]
    if lob:
        where_clauses.append(f"p.line_of_business = '{lob}'")

    where_sql = " AND ".join(where_clauses)

    results = execute_analytics_query(f"""
        SELECT
            c.claim_id,
            c.policy_id,
            c.claim_amount,
            c.anomaly_score,
            c.anomaly_layers,
            c.claim_date,
            c.status,
            c.claim_type,
            p.state,
            p.line_of_business,
            p.policyholder_name,
            p.insurer
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        WHERE {where_sql}
        ORDER BY c.anomaly_score DESC
        LIMIT {limit} OFFSET {offset}
    """)

    # Parse anomaly_layers JSON
    import json
    for r in results:
        try:
            r["anomaly_layers"] = json.loads(r.get("anomaly_layers", "{}"))
        except (json.JSONDecodeError, TypeError):
            r["anomaly_layers"] = {}
        r["badge"] = "INSIGHT"  # ADR-004: always INSIGHT, never DECISION

    return {
        "items": results,
        "total": _count_anomalies(min_score, lob),
    }


@router.get("/stats")
async def get_anomaly_stats():
    """Summary statistics for the anomaly detection pipeline."""
    results = execute_analytics_query("""
        SELECT
            COUNT(*) as total_claims,
            COUNT(CASE WHEN anomaly_score > 0.3 THEN 1 END) as flagged,
            COUNT(CASE WHEN anomaly_score > 0.6 THEN 1 END) as high_risk,
            ROUND(AVG(anomaly_score), 4) as avg_score,
            ROUND(MAX(anomaly_score), 4) as max_score
        FROM claims
    """)
    return results[0] if results else {}


@router.get("/{claim_id}")
async def get_anomaly_detail(claim_id: str):
    """Detailed anomaly breakdown for a specific claim."""
    import json
    results = execute_analytics_query(f"""
        SELECT
            c.*,
            p.policyholder_name,
            p.state,
            p.line_of_business,
            p.insurer,
            p.premium_amount,
            p.start_date as policy_start,
            p.end_date as policy_end,
            h.name as hospital_name,
            g.name as garage_name,
            a.name as agent_name,
            a.region as agent_region
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        LEFT JOIN hospitals h ON c.hospital_id = h.hospital_id
        LEFT JOIN garages g ON c.garage_id = g.garage_id
        LEFT JOIN agents a ON c.agent_id = a.agent_id
        WHERE c.claim_id = '{claim_id}'
    """)

    if not results:
        return {"error": "Claim not found"}

    result = results[0]
    try:
        result["anomaly_layers"] = json.loads(result.get("anomaly_layers", "{}"))
    except (json.JSONDecodeError, TypeError):
        result["anomaly_layers"] = {}
    result["badge"] = "INSIGHT"

    return result


def _count_anomalies(min_score: float, lob: Optional[str] = None) -> int:
    where_clauses = [f"c.anomaly_score >= {min_score}"]
    if lob:
        where_clauses.append(f"p.line_of_business = '{lob}'")
    where_sql = " AND ".join(where_clauses)

    results = execute_analytics_query(f"""
        SELECT COUNT(*) as count
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        WHERE {where_sql}
    """)
    return results[0]["count"] if results else 0
