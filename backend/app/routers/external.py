"""
ClaimLens Nexus — External Data Router (FR-009)

IRDAI and PMFBY aggregate panels alongside the synthetic core data.
Per DATA.md: these are real verified data sources, not synthetic.
"""

from fastapi import APIRouter

router = APIRouter()

# Static verified data from DATA.md (verified 2026-09-21)
# These are real figures from public sources, not synthetic data.

IRDAI_DATA = {
    "source": "IRDAI Annual Report 2024-25 / Handbook",
    "verified_date": "2026-09-21",
    "incurred_claims_ratio": {
        "fy2024_25": 82.88,
        "fy2023_24": 82.52,
        "trend": "marginally increasing",
        "unit": "percent",
    },
    "claims_settled_by_count": {
        "value": 82,
        "unit": "percent",
        "note": "Approximately 82% by number; 71.3% by value for related data",
    },
    "fraud_framework": {
        "name": "IRDAI Insurance Fraud Monitoring Framework Guidelines, 2025",
        "issued": "2025-10-09",
        "effective": "2026-04-01",
        "status": "In force for ~6 months as of Sept 2026",
        "key_requirements": [
            "Board-level Fraud Monitoring Committees",
            "FMR-1 annual reporting to IRDAI",
            "Data sharing with IIB (Insurance Information Bureau) for cross-entity pattern detection",
            "Replaces 2013 circular",
        ],
        "claimlens_relevance": (
            "ClaimLens Nexus's ring-detection approach mirrors the kind of cross-entity "
            "pattern detection the IIB mandate is pushing insurers toward — a more specific "
            "and stronger pitch than generic 'AI for insurance' framing."
        ),
    },
}

PMFBY_DATA = {
    "source": "PMFBY Dashboard / PIB Press Notes / data.gov.in",
    "verified_date": "2026-09-21",
    "national_summary": {
        "total_applications": "56.96 crore",
        "total_claims_paid": "₹1.54 lakh crore",
        "note": "National-level PMFBY summary stats from PIB press notes",
    },
    "state_claims_paid": {
        "source": "data.gov.in — PMFBY state/UT claims paid, 2019-20 to 2023-24",
        "license": "Government Open Data License",
        "coverage_note": (
            "Several near-duplicate resources exist on data.gov.in with different year windows. "
            "Some states (West Bengal, Gujarat, Jharkhand) show 'NA' in some years."
        ),
    },
}


@router.get("/irdai")
async def get_irdai_panel():
    """
    IRDAI regulatory context panel.
    Per DATA.md: these are verified figures from public government reports.
    """
    return IRDAI_DATA


@router.get("/pmfby")
async def get_pmfby_panel():
    """
    PMFBY (Pradhan Mantri Fasal Bima Yojana) context panel.
    Per DATA.md: national-level summary from verified public sources.
    """
    return PMFBY_DATA
