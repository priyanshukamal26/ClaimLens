"""
ClaimLens Nexus — Trends Router (FR-002)

Executive Overview: monthly claims/premium/loss ratio by line of business & state.
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.database import execute_analytics_query

router = APIRouter()


@router.get("/overview")
async def get_overview():
    """KPI summary for the Executive Overview hero band."""
    results = execute_analytics_query("""
        SELECT
            COUNT(DISTINCT p.policy_id) as total_policies,
            COUNT(DISTINCT c.claim_id) as total_claims,
            ROUND(SUM(p.premium_amount), 2) as total_premium,
            ROUND(
                COALESCE(SUM(c.claim_amount), 0) / NULLIF(SUM(p.premium_amount), 0) * 100,
                2
            ) as loss_ratio,
            ROUND(
                COUNT(CASE WHEN c.status = 'Approved' THEN 1 END) * 100.0 /
                NULLIF(COUNT(c.claim_id), 0),
                2
            ) as settlement_rate,
            COUNT(CASE WHEN c.anomaly_score > 0.3 THEN 1 END) as anomalies_flagged
        FROM policies p
        LEFT JOIN claims c ON p.policy_id = c.policy_id
    """)
    return results[0] if results else {}


@router.get("/monthly")
async def get_monthly_trends(
    lob: Optional[str] = Query(None, description="Filter by line of business"),
    state: Optional[str] = Query(None, description="Filter by state"),
):
    """Monthly trend data for claims, premiums, and loss ratio."""
    where_clauses = []
    if lob:
        where_clauses.append(f"p.line_of_business = '{lob}'")
    if state:
        where_clauses.append(f"p.state = '{state}'")

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    results = execute_analytics_query(f"""
        SELECT
            substr(c.claim_date, 1, 7) as month,
            COUNT(c.claim_id) as claims_count,
            ROUND(SUM(p.premium_amount), 2) as premium_amount,
            ROUND(
                SUM(c.claim_amount) / NULLIF(SUM(p.premium_amount), 0) * 100,
                2
            ) as loss_ratio,
            COUNT(CASE WHEN c.status = 'Approved' THEN 1 END) as settlement_count
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        {where_sql}
        GROUP BY substr(c.claim_date, 1, 7)
        ORDER BY month
    """)
    return results


@router.get("/by-lob")
async def get_trends_by_lob():
    """Breakdown by line of business."""
    results = execute_analytics_query("""
        SELECT
            p.line_of_business,
            COUNT(c.claim_id) as claims_count,
            ROUND(SUM(c.claim_amount), 2) as total_claims_amount,
            ROUND(SUM(p.premium_amount), 2) as total_premium,
            ROUND(
                SUM(c.claim_amount) / NULLIF(SUM(p.premium_amount), 0) * 100,
                2
            ) as loss_ratio,
            COUNT(CASE WHEN c.anomaly_score > 0.3 THEN 1 END) as anomalies_flagged
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        GROUP BY p.line_of_business
        ORDER BY claims_count DESC
    """)
    return results


@router.get("/by-state")
async def get_trends_by_state():
    """Breakdown by state."""
    results = execute_analytics_query("""
        SELECT
            p.state,
            COUNT(c.claim_id) as claims_count,
            ROUND(SUM(c.claim_amount), 2) as total_claims_amount,
            ROUND(SUM(p.premium_amount), 2) as total_premium,
            ROUND(
                SUM(c.claim_amount) / NULLIF(SUM(p.premium_amount), 0) * 100,
                2
            ) as loss_ratio,
            COUNT(CASE WHEN c.anomaly_score > 0.3 THEN 1 END) as anomalies_flagged
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        GROUP BY p.state
        ORDER BY claims_count DESC
        LIMIT 15
    """)
    return results
