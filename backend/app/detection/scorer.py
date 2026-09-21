"""
ClaimLens Nexus — Combined Anomaly Scorer

Orchestrates the three-layer detection pipeline (ADR-001) and writes
combined scores back to the database.
"""

import json
from app.database import sqlite_session
from app.detection.rules_engine import run_rules_engine
from app.detection.isolation_forest import run_isolation_forest
from app.detection.graph_community import run_graph_community_detection


# Layer weights for combining scores
LAYER_WEIGHTS = {
    "rules": 0.35,
    "isolation_forest": 0.35,
    "graph_community": 0.30,
}


def run_full_detection_pipeline():
    """
    Run all three anomaly detection layers and write combined scores to the database.
    Called during application startup after data is loaded.
    """
    print("Running three-layer anomaly detection pipeline...")

    # Load data from SQLite
    with sqlite_session() as conn:
        claims = [dict(row) for row in conn.execute("SELECT * FROM claims").fetchall()]
        policies = [dict(row) for row in conn.execute("SELECT * FROM policies").fetchall()]
        hospitals = [dict(row) for row in conn.execute("SELECT * FROM hospitals").fetchall()]
        garages = [dict(row) for row in conn.execute("SELECT * FROM garages").fetchall()]
        agents = [dict(row) for row in conn.execute("SELECT * FROM agents").fetchall()]

    if not claims:
        print("No claims to score.")
        return

    # Layer 1: Rules Engine
    print("  Layer 1: Rules engine...")
    rules_scores = run_rules_engine(claims, policies)

    # Layer 2: Isolation Forest
    print("  Layer 2: Isolation Forest...")
    iforest_scores = run_isolation_forest(claims, policies)

    # Layer 3: Graph/Louvain Community Detection
    print("  Layer 3: Graph/Louvain community detection...")
    graph_scores = run_graph_community_detection(claims, hospitals, garages, agents)

    # Combine scores
    print("  Combining scores...")
    combined_scores = {}
    for claim in claims:
        cid = claim["claim_id"]
        rules_s = rules_scores.get(cid, 0.0)
        iforest_s = iforest_scores.get(cid, 0.0)
        graph_s = graph_scores.get(cid, 0.0)

        # Weighted combination
        combined = (
            LAYER_WEIGHTS["rules"] * rules_s +
            LAYER_WEIGHTS["isolation_forest"] * iforest_s +
            LAYER_WEIGHTS["graph_community"] * graph_s
        )

        layer_detail = {
            "rules": round(rules_s, 4),
            "isolation_forest": round(iforest_s, 4),
            "graph_community": round(graph_s, 4),
        }

        combined_scores[cid] = {
            "score": round(combined, 4),
            "layers": layer_detail,
        }

    # Write scores back to SQLite
    with sqlite_session() as conn:
        for cid, data in combined_scores.items():
            conn.execute(
                "UPDATE claims SET anomaly_score = ?, anomaly_layers = ? WHERE claim_id = ?",
                (data["score"], json.dumps(data["layers"]), cid)
            )

    # Stats
    flagged = sum(1 for d in combined_scores.values() if d["score"] > 0.3)
    high_risk = sum(1 for d in combined_scores.values() if d["score"] > 0.6)
    print(f"  Detection complete: {flagged} claims flagged (score > 0.3), "
          f"{high_risk} high-risk (score > 0.6)")
