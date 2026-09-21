"""
ClaimLens Nexus — Layer 1: Rules Engine

Interpretable, explicit fraud-indicator rules. This is the most transparent
layer of the three-layer detection system (ADR-001).

Rules are derived from the fraud patterns documented in seed_data.py.
"""

from datetime import datetime, timedelta
from collections import defaultdict


def run_rules_engine(claims: list[dict], policies: list[dict]) -> dict[str, float]:
    """
    Score each claim against a set of interpretable fraud rules.

    Returns: {claim_id: score} where score is 0.0 to 1.0
    """
    scores = {}
    policy_map = {p["policy_id"]: p for p in policies}

    # Pre-compute per-LOB averages for spike detection
    lob_amounts = defaultdict(list)
    for c in claims:
        p = policy_map.get(c["policy_id"])
        if p:
            lob_amounts[p["line_of_business"]].append(c["claim_amount"])

    lob_avg = {lob: sum(amounts) / len(amounts) for lob, amounts in lob_amounts.items()}

    # Pre-compute claims per policy for rapid-repeat detection
    claims_per_policy = defaultdict(list)
    for c in claims:
        claims_per_policy[c["policy_id"]].append(c)

    for claim in claims:
        rule_hits = []
        policy = policy_map.get(claim["policy_id"])

        if not policy:
            scores[claim["claim_id"]] = 0.0
            continue

        lob = policy["line_of_business"]

        # Rule 1: Amount spike — claim > 5x LOB average
        if lob in lob_avg and claim["claim_amount"] > 5 * lob_avg[lob]:
            rule_hits.append(("amount_spike", 0.35))

        # Rule 2: Rapid repeat — multiple claims same policy within 30 days
        policy_claims = claims_per_policy.get(claim["policy_id"], [])
        claim_dt = datetime.strptime(claim["claim_date"], "%Y-%m-%d")
        nearby_claims = [
            c for c in policy_claims
            if c["claim_id"] != claim["claim_id"]
            and abs((datetime.strptime(c["claim_date"], "%Y-%m-%d") - claim_dt).days) <= 30
        ]
        if len(nearby_claims) >= 2:
            rule_hits.append(("rapid_repeat", 0.30))
        elif len(nearby_claims) == 1:
            rule_hits.append(("rapid_repeat", 0.15))

        # Rule 3: New policy claim — within 15 days of policy start
        policy_start = datetime.strptime(policy["start_date"], "%Y-%m-%d")
        days_from_start = (claim_dt - policy_start).days
        if 0 <= days_from_start <= 15:
            rule_hits.append(("new_policy_claim", 0.25))

        # Rule 4: Mismatched LOB — health claim through garage or motor through hospital only
        if lob == "Health" and claim.get("garage_id") and not claim.get("hospital_id"):
            rule_hits.append(("mismatched_lob", 0.40))
        elif lob == "Motor" and claim.get("hospital_id") and not claim.get("garage_id"):
            if claim["claim_type"] != "Third-Party":  # Third-party motor can involve hospitals
                rule_hits.append(("mismatched_lob", 0.30))

        # Rule 5: Weekend claim with rapid settlement (< 7 days)
        claim_weekday = datetime.strptime(claim["claim_date"], "%Y-%m-%d").weekday()
        if claim_weekday >= 5 and claim.get("settlement_date"):  # Weekend
            settle_dt = datetime.strptime(claim["settlement_date"], "%Y-%m-%d")
            if (settle_dt - claim_dt).days < 7:
                rule_hits.append(("weekend_rapid_settle", 0.20))

        # Rule 6: Very high claim amount (top 1% absolute)
        if claim["claim_amount"] > 1500000:
            rule_hits.append(("high_absolute_amount", 0.15))

        # Combine rule scores: take max + sum of others * 0.3 (diminishing returns)
        if rule_hits:
            rule_hits.sort(key=lambda x: x[1], reverse=True)
            score = rule_hits[0][1]
            for _, s in rule_hits[1:]:
                score += s * 0.3
            score = min(score, 1.0)
        else:
            score = 0.0

        scores[claim["claim_id"]] = round(score, 4)

    return scores
