"""
ClaimLens Nexus — Decisions Router (FR-006)

Decision Log: records human decisions made on insights.
Per ADR-004: insights and decisions are kept visually and data-model separate.

Live-sync fix: list_decisions and get_decision_stats now read from SQLite
(the operational transactional store) so newly recorded decisions appear
immediately without waiting for a DuckDB analytics-layer reload.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Optional
from app.database import sqlite_session, execute_analytics_query

router = APIRouter()


class DecisionCreate(BaseModel):
    claim_id: str
    insight_type: str  # Anomaly, Pattern, Ring
    decision_type: str  # Investigate, Escalate, Dismiss, Approve
    decided_by: str
    rationale: Optional[str] = None


@router.get("/")
async def list_decisions(
    limit: int = 50,
    offset: int = 0,
):
    """List all decisions in the Decision Log — reads from SQLite for live sync."""
    with sqlite_session() as conn:
        cursor = conn.execute(f"""
            SELECT
                d.decision_id,
                d.claim_id,
                d.insight_type,
                d.decision_type,
                d.decided_by,
                d.decided_at,
                d.rationale,
                c.claim_amount,
                c.anomaly_score,
                c.claim_date,
                p.line_of_business,
                p.state,
                p.policyholder_name
            FROM decisions d
            JOIN claims c ON d.claim_id = c.claim_id
            JOIN policies p ON c.policy_id = p.policy_id
            ORDER BY d.decided_at DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
    return {"items": results}


@router.post("/")
async def create_decision(decision: DecisionCreate):
    """
    Record a human decision on a flagged insight.

    This is the explicit point where an INSIGHT becomes a DECISION —
    the human decides, the system does not.
    """
    decision_id = f"DEC-{uuid.uuid4().hex[:8].upper()}"
    decided_at = datetime.now().isoformat()

    with sqlite_session() as conn:
        conn.execute(
            "INSERT INTO decisions VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                decision_id,
                decision.claim_id,
                decision.insight_type,
                decision.decision_type,
                decision.decided_by,
                decided_at,
                decision.rationale,
            )
        )

    return {
        "decision_id": decision_id,
        "decided_at": decided_at,
        "message": "Decision recorded successfully.",
    }


@router.get("/stats")
async def get_decision_stats():
    """Summary statistics for the Decision Log — reads from SQLite for live sync."""
    with sqlite_session() as conn:
        cursor = conn.execute("""
            SELECT
                COUNT(*) as total_decisions,
                COUNT(CASE WHEN decision_type = 'Investigate' THEN 1 END) as investigate,
                COUNT(CASE WHEN decision_type = 'Escalate' THEN 1 END) as escalate,
                COUNT(CASE WHEN decision_type = 'Dismiss' THEN 1 END) as dismiss,
                COUNT(CASE WHEN decision_type = 'Approve' THEN 1 END) as approve
            FROM decisions
        """)
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        result = dict(zip(columns, row)) if row else {}
    return result

