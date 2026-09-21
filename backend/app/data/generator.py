"""
ClaimLens Nexus — Synthetic Data Generator

Generates realistic Indian insurance data: policies, claims, hospitals, garages, agents.
Calibrated against verified IRDAI figures from DATA.md:
  - Non-life incurred claims ratio: ~82.88%
  - Claims settled by count: ~82%

Per DATA.md: No public India-specific claim-level fraud dataset exists.
This generator creates synthetic data with realistic distributions and
deliberately injects fraud patterns for the P4 held-out evaluation.
"""

import random
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional

from app.config import (
    SYNTHETIC_POLICIES_COUNT, SYNTHETIC_CLAIMS_COUNT,
    SYNTHETIC_HOSPITALS_COUNT, SYNTHETIC_GARAGES_COUNT, SYNTHETIC_AGENTS_COUNT,
    CALIBRATION_CLAIMS_RATIO, CALIBRATION_SETTLEMENT_RATE,
)
from app.data.seed_data import (
    STATES, STATE_CITIES, LINES_OF_BUSINESS, LOB_WEIGHTS, LOB_CLAIM_TYPES,
    INSURERS, TPA_NETWORKS, HOSPITAL_PREFIXES, HOSPITAL_SUFFIXES,
    GARAGE_PREFIXES, GARAGE_TYPES, FIRST_NAMES, LAST_NAMES,
    PREMIUM_RANGES, CLAIM_AMOUNT_RANGES, FRAUD_PATTERNS,
)


class SyntheticDataGenerator:
    """Generates all synthetic data for ClaimLens Nexus."""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2025, 9, 1)

    def _random_date(self, start: datetime, end: datetime) -> str:
        delta = (end - start).days
        random_days = self.rng.randint(0, max(0, delta))
        return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

    def _weighted_choice(self, options: list, weights: list) -> str:
        return self.rng.choices(options, weights=weights, k=1)[0]

    def _random_name(self) -> str:
        return f"{self.rng.choice(FIRST_NAMES)} {self.rng.choice(LAST_NAMES)}"

    def _random_state(self) -> str:
        # Weight toward high-population states
        weights = [15, 12, 12, 10, 10, 8, 6, 6, 6, 5,
                   4, 4, 3, 3, 3, 2, 2, 1, 1, 1,
                   1, 1, 1, 1]
        return self._weighted_choice(STATES, weights)

    def _random_city(self, state: str) -> str:
        cities = STATE_CITIES.get(state, ["Unknown"])
        return self.rng.choice(cities)

    # ---- Hospitals ----
    def generate_hospitals(self) -> list[dict]:
        hospitals = []
        for i in range(SYNTHETIC_HOSPITALS_COUNT):
            state = self._random_state()
            hospitals.append({
                "hospital_id": f"HOSP-{i+1:04d}",
                "name": f"{self.rng.choice(HOSPITAL_PREFIXES)} {self.rng.choice(HOSPITAL_SUFFIXES)}",
                "city": self._random_city(state),
                "state": state,
                "tpa_network": self.rng.choice(TPA_NETWORKS) if self.rng.random() < 0.7 else None,
                "bed_count": self.rng.randint(20, 500),
            })
        return hospitals

    # ---- Garages ----
    def generate_garages(self) -> list[dict]:
        garages = []
        for i in range(SYNTHETIC_GARAGES_COUNT):
            state = self._random_state()
            garages.append({
                "garage_id": f"GAR-{i+1:04d}",
                "name": f"{self.rng.choice(GARAGE_PREFIXES)} - {self._random_city(state)}",
                "city": self._random_city(state),
                "state": state,
                "service_type": self.rng.choice(GARAGE_TYPES),
            })
        return garages

    # ---- Agents ----
    def generate_agents(self) -> list[dict]:
        agents = []
        for i in range(SYNTHETIC_AGENTS_COUNT):
            agents.append({
                "agent_id": f"AGT-{i+1:04d}",
                "name": self._random_name(),
                "region": self._random_state(),
                "commission_rate": round(self.rng.uniform(0.05, 0.20), 3),
                "active_policies_count": 0,  # will be updated after policy generation
            })
        return agents

    # ---- Policies ----
    def generate_policies(self, agents: list[dict]) -> list[dict]:
        policies = []
        lob_list = list(LOB_WEIGHTS.keys())
        lob_weight_list = list(LOB_WEIGHTS.values())
        agent_ids = [a["agent_id"] for a in agents]
        agent_policy_counts = {a: 0 for a in agent_ids}

        for i in range(SYNTHETIC_POLICIES_COUNT):
            lob = self._weighted_choice(lob_list, lob_weight_list)
            premium_min, premium_max = PREMIUM_RANGES[lob]
            start = self._random_date(self.start_date, self.end_date - timedelta(days=365))
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = start_dt + timedelta(days=365)
            agent_id = self.rng.choice(agent_ids)
            agent_policy_counts[agent_id] += 1

            # Status distribution
            status_roll = self.rng.random()
            if start_dt + timedelta(days=365) < datetime.now():
                status = "Expired" if status_roll < 0.85 else "Cancelled"
            else:
                status = "Active" if status_roll < 0.90 else "Cancelled"

            policies.append({
                "policy_id": f"POL-{i+1:06d}",
                "policyholder_name": self._random_name(),
                "state": self._random_state(),
                "line_of_business": lob,
                "insurer": self.rng.choice(INSURERS),
                "premium_amount": round(self.rng.uniform(premium_min, premium_max), 2),
                "start_date": start,
                "end_date": end_dt.strftime("%Y-%m-%d"),
                "status": status,
            })

        # Update agent policy counts
        for agent in agents:
            agent["active_policies_count"] = agent_policy_counts.get(agent["agent_id"], 0)

        return policies

    # ---- Claims ----
    def generate_claims(
        self,
        policies: list[dict],
        hospitals: list[dict],
        garages: list[dict],
        agents: list[dict],
    ) -> list[dict]:
        claims = []
        hospital_ids = [h["hospital_id"] for h in hospitals]
        garage_ids = [g["garage_id"] for g in garages]
        agent_ids = [a["agent_id"] for a in agents]

        # Build a map of policies by LOB for realistic claims
        policies_by_lob = {}
        for p in policies:
            policies_by_lob.setdefault(p["line_of_business"], []).append(p)

        # Fraud injection: ~5% of claims will have fraud patterns
        fraud_count = int(SYNTHETIC_CLAIMS_COUNT * 0.05)
        fraud_indices = set(self.rng.sample(range(SYNTHETIC_CLAIMS_COUNT), fraud_count))

        for i in range(SYNTHETIC_CLAIMS_COUNT):
            # Pick a policy (weighted toward active/expired, not cancelled)
            policy = self.rng.choice(policies)
            while policy["status"] == "Cancelled" and self.rng.random() < 0.8:
                policy = self.rng.choice(policies)

            lob = policy["line_of_business"]
            claim_types = LOB_CLAIM_TYPES[lob]
            claim_type = self.rng.choice(claim_types)
            amt_min, amt_max = CLAIM_AMOUNT_RANGES[lob]

            is_fraud = i in fraud_indices
            fraud_flag = 1 if is_fraud else 0

            # Claim amount — fraud claims tend to be higher
            if is_fraud and self.rng.random() < 0.6:
                # Spike pattern: unusually high claim
                claim_amount = round(self.rng.uniform(amt_max * 0.7, amt_max * 2.0), 2)
            else:
                # Log-normal-ish distribution (most claims are smaller)
                claim_amount = round(
                    amt_min + (amt_max - amt_min) * (self.rng.paretovariate(2.0) - 1) / 4,
                    2
                )
                claim_amount = max(amt_min, min(claim_amount, amt_max * 1.5))

            # Claim date: after policy start, before policy end or now
            policy_start = datetime.strptime(policy["start_date"], "%Y-%m-%d")
            policy_end = datetime.strptime(policy["end_date"], "%Y-%m-%d")
            claim_date_end = min(policy_end, self.end_date)

            if is_fraud and self.rng.random() < 0.3:
                # New-policy-claim pattern: within 15 days of start
                claim_date = self._random_date(
                    policy_start,
                    min(policy_start + timedelta(days=15), claim_date_end)
                )
            else:
                claim_date = self._random_date(policy_start, claim_date_end)

            # Settlement: ~82% settled (per calibration)
            settled = self.rng.random() < CALIBRATION_SETTLEMENT_RATE
            if settled:
                status = "Approved"
                settlement_amount = round(claim_amount * self.rng.uniform(0.5, 1.0), 2)
                claim_dt = datetime.strptime(claim_date, "%Y-%m-%d")
                settlement_date = self._random_date(
                    claim_dt + timedelta(days=7),
                    min(claim_dt + timedelta(days=180), self.end_date)
                )
            else:
                status_roll = self.rng.random()
                if status_roll < 0.4:
                    status = "Pending"
                elif status_roll < 0.7:
                    status = "Rejected"
                else:
                    status = "Under Investigation"
                settlement_amount = None
                settlement_date = None

            # Hospital/garage assignment based on LOB
            hospital_id = None
            garage_id = None
            if lob == "Health":
                hospital_id = self.rng.choice(hospital_ids)
                # Fraud: mismatched LOB pattern (health claim through garage)
                if is_fraud and self.rng.random() < 0.15:
                    garage_id = self.rng.choice(garage_ids)
            elif lob == "Motor":
                garage_id = self.rng.choice(garage_ids)
                if claim_type == "Third-Party":
                    hospital_id = self.rng.choice(hospital_ids) if self.rng.random() < 0.3 else None
            else:
                if self.rng.random() < 0.2:
                    hospital_id = self.rng.choice(hospital_ids)

            # Agent: fraud rings tend to cluster through same agents
            if is_fraud and self.rng.random() < 0.4:
                # Use a small pool of "ring" agents
                ring_agents = agent_ids[:5]
                agent_id = self.rng.choice(ring_agents)
            else:
                agent_id = self.rng.choice(agent_ids)

            claims.append({
                "claim_id": f"CLM-{i+1:06d}",
                "policy_id": policy["policy_id"],
                "claim_amount": claim_amount,
                "claim_date": claim_date,
                "settlement_amount": settlement_amount,
                "settlement_date": settlement_date,
                "status": status,
                "hospital_id": hospital_id,
                "garage_id": garage_id,
                "agent_id": agent_id,
                "claim_type": claim_type,
                "fraud_flag": fraud_flag,
                "anomaly_score": 0.0,
                "anomaly_layers": "{}",
            })

        return claims

    def generate_all(self) -> dict:
        """Generate all synthetic data."""
        print("Generating hospitals...")
        hospitals = self.generate_hospitals()

        print("Generating garages...")
        garages = self.generate_garages()

        print("Generating agents...")
        agents = self.generate_agents()

        print("Generating policies...")
        policies = self.generate_policies(agents)

        print("Generating claims...")
        claims = self.generate_claims(policies, hospitals, garages, agents)

        print(f"Generated: {len(policies)} policies, {len(claims)} claims, "
              f"{len(hospitals)} hospitals, {len(garages)} garages, {len(agents)} agents")

        fraud_count = sum(1 for c in claims if c["fraud_flag"] == 1)
        print(f"Fraud-flagged claims (for P4 eval): {fraud_count} ({fraud_count/len(claims)*100:.1f}%)")

        return {
            "policies": policies,
            "claims": claims,
            "hospitals": hospitals,
            "garages": garages,
            "agents": agents,
        }
