"""
ClaimLens Nexus — Layer 2: Isolation Forest

Statistical outlier detection using scikit-learn's Isolation Forest.
Per ADR-001: catches statistical outliers that interpretable rules miss.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime


def run_isolation_forest(claims: list[dict], policies: list[dict]) -> dict[str, float]:
    """
    Score each claim using Isolation Forest on numeric features.

    Returns: {claim_id: score} where score is 0.0 to 1.0
    (higher = more anomalous)
    """
    if not claims:
        return {}

    policy_map = {p["policy_id"]: p for p in policies}

    # Build feature matrix
    features = []
    claim_ids = []

    for claim in claims:
        policy = policy_map.get(claim["policy_id"])
        if not policy:
            continue

        claim_dt = datetime.strptime(claim["claim_date"], "%Y-%m-%d")
        policy_start = datetime.strptime(policy["start_date"], "%Y-%m-%d")

        feature_vec = [
            claim["claim_amount"],
            policy["premium_amount"],
            # Claim-to-premium ratio
            claim["claim_amount"] / max(policy["premium_amount"], 1),
            # Days from policy start to claim
            (claim_dt - policy_start).days,
            # Settlement ratio (0 if no settlement)
            (claim.get("settlement_amount") or 0) / max(claim["claim_amount"], 1),
            # Day of week (0-6)
            claim_dt.weekday(),
            # Month
            claim_dt.month,
        ]
        features.append(feature_vec)
        claim_ids.append(claim["claim_id"])

    if len(features) < 10:
        return {cid: 0.0 for cid in claim_ids}

    X = np.array(features)

    # Fit Isolation Forest
    iso_forest = IsolationForest(
        n_estimators=100,
        contamination=0.05,  # Expect ~5% anomalies
        random_state=42,
        n_jobs=-1,
    )
    iso_forest.fit(X)

    # Get anomaly scores
    # decision_function: negative = anomalous, positive = normal
    raw_scores = iso_forest.decision_function(X)

    # Normalize to 0-1 range (higher = more anomalous)
    min_score = raw_scores.min()
    max_score = raw_scores.max()
    score_range = max_score - min_score

    if score_range == 0:
        normalized = np.zeros_like(raw_scores)
    else:
        # Invert so that lower raw scores (more anomalous) map to higher normalized scores
        normalized = (max_score - raw_scores) / score_range

    scores = {}
    for i, claim_id in enumerate(claim_ids):
        scores[claim_id] = round(float(normalized[i]), 4)

    return scores
