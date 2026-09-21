"""
ClaimLens Nexus — Layer 3: Graph / Louvain Community Detection

Relational pattern detection across entities (agent-hospital-claim rings).
Per ADR-001: catches collusion patterns that neither rules nor statistical
outlier detection would identify independently.

Uses networkx for graph construction and community-louvain for Louvain
community detection.
"""

import networkx as nx
import community as community_louvain
from collections import defaultdict


def run_graph_community_detection(
    claims: list[dict],
    hospitals: list[dict],
    garages: list[dict],
    agents: list[dict],
) -> dict[str, float]:
    """
    Build an entity-relationship graph and detect suspicious communities.

    Graph nodes: agents, hospitals, garages
    Graph edges: weighted by number of claims connecting them

    A tight community (high modularity cluster) with many claims flowing
    through the same agent-hospital or agent-garage pair is suspicious.

    Returns: {claim_id: score} where score is 0.0 to 1.0
    """
    if not claims:
        return {}

    # Build the entity graph
    G = nx.Graph()

    # Track edge weights (number of claims on each edge)
    edge_claims = defaultdict(list)  # (node1, node2) -> [claim_ids]

    for claim in claims:
        agent_id = claim.get("agent_id")
        hospital_id = claim.get("hospital_id")
        garage_id = claim.get("garage_id")

        # Add edges between connected entities
        if agent_id and hospital_id:
            edge_key = (f"agent:{agent_id}", f"hospital:{hospital_id}")
            edge_claims[edge_key].append(claim["claim_id"])

        if agent_id and garage_id:
            edge_key = (f"agent:{agent_id}", f"garage:{garage_id}")
            edge_claims[edge_key].append(claim["claim_id"])

        if hospital_id and garage_id:
            edge_key = (f"hospital:{hospital_id}", f"garage:{garage_id}")
            edge_claims[edge_key].append(claim["claim_id"])

    # Add weighted edges to graph
    for (n1, n2), claim_list in edge_claims.items():
        G.add_edge(n1, n2, weight=len(claim_list), claims=claim_list)

    if G.number_of_edges() == 0:
        return {c["claim_id"]: 0.0 for c in claims}

    # Run Louvain community detection
    try:
        partition = community_louvain.best_partition(G, random_state=42)
    except Exception:
        return {c["claim_id"]: 0.0 for c in claims}

    # Identify suspicious communities:
    # - Small, tight communities with disproportionately many claims
    community_nodes = defaultdict(list)
    for node, comm_id in partition.items():
        community_nodes[comm_id].append(node)

    # Calculate suspicion score per community
    community_scores = {}
    total_claims_in_graph = sum(len(cl) for cl in edge_claims.values())

    for comm_id, nodes in community_nodes.items():
        if len(nodes) < 2:
            community_scores[comm_id] = 0.0
            continue

        # Count claims in this community
        comm_claims = set()
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                if G.has_edge(n1, n2):
                    comm_claims.update(G[n1][n2].get("claims", []))

        if not comm_claims:
            community_scores[comm_id] = 0.0
            continue

        # Suspicion: high claim density relative to community size
        # A community with few nodes but many claims is suspicious
        density = len(comm_claims) / max(len(nodes), 1)
        expected_density = total_claims_in_graph / max(G.number_of_nodes(), 1)

        if expected_density > 0:
            suspicion_ratio = density / expected_density
        else:
            suspicion_ratio = 0

        # Normalize to 0-1 (cap at ratio of 5x expected)
        score = min(suspicion_ratio / 5.0, 1.0)
        community_scores[comm_id] = round(score, 4)

    # Map scores back to claims
    # A claim gets the score of its community
    claim_community = {}
    for claim in claims:
        agent_id = claim.get("agent_id")
        hospital_id = claim.get("hospital_id")
        garage_id = claim.get("garage_id")

        # Find which community this claim's entities belong to
        best_score = 0.0
        for entity_id in [f"agent:{agent_id}", f"hospital:{hospital_id}", f"garage:{garage_id}"]:
            if entity_id in partition:
                comm_id = partition[entity_id]
                best_score = max(best_score, community_scores.get(comm_id, 0.0))

        claim_community[claim["claim_id"]] = best_score

    return claim_community
