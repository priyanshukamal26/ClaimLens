"""
ClaimLens Nexus — Pydantic Schemas for All Entities

Per MASTER.md: entities are policies, claims, hospitals, garages, agents.
Per DATA.md: calibrated against verified IRDAI figures.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date


class Policy(BaseModel):
    policy_id: str
    policyholder_name: str
    state: str
    line_of_business: str  # Health, Motor, Fire, Marine, Misc
    insurer: str
    premium_amount: float
    start_date: str
    end_date: str
    status: str = "Active"  # Active, Expired, Cancelled


class Claim(BaseModel):
    claim_id: str
    policy_id: str
    claim_amount: float
    claim_date: str
    settlement_amount: Optional[float] = None
    settlement_date: Optional[str] = None
    status: str = "Pending"  # Pending, Approved, Rejected, Under Investigation
    hospital_id: Optional[str] = None
    garage_id: Optional[str] = None
    agent_id: Optional[str] = None
    claim_type: str  # Cashless, Reimbursement, Third-Party, Own Damage
    fraud_flag: int = 0  # 0 = no fraud, 1 = fraud (for P4 held-out eval)
    anomaly_score: float = 0.0
    anomaly_layers: str = "{}"  # JSON string with per-layer scores


class Hospital(BaseModel):
    hospital_id: str
    name: str
    city: str
    state: str
    tpa_network: Optional[str] = None
    bed_count: Optional[int] = None


class Garage(BaseModel):
    garage_id: str
    name: str
    city: str
    state: str
    service_type: str  # Authorized, Multi-brand, Specialist


class Agent(BaseModel):
    agent_id: str
    name: str
    region: str
    commission_rate: float
    active_policies_count: int = 0


class Decision(BaseModel):
    decision_id: str
    claim_id: str
    insight_type: str  # Anomaly, Pattern, Ring
    decision_type: str  # Investigate, Escalate, Dismiss, Approve
    decided_by: str
    decided_at: str
    rationale: Optional[str] = None


# --- API Response Models ---

class KPIData(BaseModel):
    total_policies: int
    total_claims: int
    total_premium: float
    loss_ratio: float
    settlement_rate: float
    anomalies_flagged: int


class TrendPoint(BaseModel):
    month: str
    claims_count: int
    premium_amount: float
    loss_ratio: float
    settlement_count: int


class AnomalyItem(BaseModel):
    claim_id: str
    policy_id: str
    claim_amount: float
    anomaly_score: float
    anomaly_layers: dict
    claim_date: str
    status: str
    claim_type: str
    state: str
    line_of_business: str


class AskResponse(BaseModel):
    answer: str
    sql_used: Optional[str] = None
    source: str  # "live_llm", "cache", "golden_query", "template"
    is_insight: bool = True  # Always True — per ADR-004, never a decision


class MorningBrief(BaseModel):
    date: str
    summary: str
    top_anomalies: list[AnomalyItem]
    kpi_snapshot: KPIData
    trend_direction: str  # "improving", "stable", "worsening"
