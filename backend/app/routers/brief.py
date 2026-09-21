"""
ClaimLens Nexus — Morning Brief Router (FR-005)

Synthesized daily summary of key metrics and top anomalies.
"""

from fastapi import APIRouter
from datetime import datetime
from app.database import execute_analytics_query

router = APIRouter()


@router.get("/morning")
async def get_morning_brief():
    """
    Morning Brief: synthesized daily summary.

    Per FR-005: supports faster decision-making through a ranked review queue,
    gain chart, and this Morning Brief.
    """
    today = datetime.now().strftime("%Y-%m-%d")

    # KPI snapshot
    kpi = execute_analytics_query("""
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
    kpi_data = kpi[0] if kpi else {}

    # Top anomalies
    top_anomalies = execute_analytics_query("""
        SELECT
            c.claim_id,
            c.claim_amount,
            c.anomaly_score,
            c.claim_date,
            c.status,
            c.claim_type,
            p.state,
            p.line_of_business,
            p.policyholder_name
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        WHERE c.anomaly_score > 0.3
        ORDER BY c.anomaly_score DESC
        LIMIT 5
    """)

    # Trend direction (compare last 2 months)
    monthly = execute_analytics_query("""
        SELECT
            substr(c.claim_date, 1, 7) as month,
            ROUND(SUM(c.claim_amount) / NULLIF(SUM(p.premium_amount), 0) * 100, 2) as loss_ratio
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        GROUP BY month
        ORDER BY month DESC
        LIMIT 2
    """)

    if len(monthly) >= 2:
        current_lr = monthly[0].get("loss_ratio", 0) or 0
        previous_lr = monthly[1].get("loss_ratio", 0) or 0
        if current_lr > previous_lr * 1.05:
            trend = "worsening"
        elif current_lr < previous_lr * 0.95:
            trend = "improving"
        else:
            trend = "stable"
    else:
        trend = "stable"

    # Build summary narrative
    anomaly_count = kpi_data.get("anomalies_flagged", 0)
    loss_ratio = kpi_data.get("loss_ratio", 0)

    summary = (
        f"Good morning. As of today, ClaimLens Nexus is monitoring "
        f"{kpi_data.get('total_policies', 0):,} policies with "
        f"{kpi_data.get('total_claims', 0):,} claims processed. "
        f"The current loss ratio stands at {loss_ratio:.1f}%, "
        f"which is {trend} compared to the prior period. "
        f"{anomaly_count} claims have been flagged as insights requiring review. "
        f"The top flagged item has an anomaly score of "
        f"{top_anomalies[0]['anomaly_score']:.2f} "
        f"(₹{top_anomalies[0]['claim_amount']:,.0f} — {top_anomalies[0]['line_of_business']})."
        if top_anomalies else
        f"No significant anomalies detected in the current review period."
    )

    return {
        "date": today,
        "summary": summary,
        "top_anomalies": top_anomalies,
        "kpi_snapshot": kpi_data,
        "trend_direction": trend,
    }
