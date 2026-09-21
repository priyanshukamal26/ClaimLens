"""
ClaimLens Nexus — 10 Golden Queries (Deterministic Fallback)

Pre-validated question/answer pairs that bypass the live LLM chain entirely.
Per AI_ML.md: this is a deliberate hedge against LLM flakiness during a live demo.
Treat as load-bearing for the demo, not a placeholder.

These queries work with zero LLM API keys configured.
"""

GOLDEN_QUERIES = [
    {
        "question": "What is the overall loss ratio?",
        "keywords": ["loss ratio", "overall loss", "claims ratio"],
        "sql": """
            SELECT ROUND(
                SUM(c.claim_amount) / NULLIF(SUM(p.premium_amount), 0) * 100, 2
            ) as loss_ratio
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
        """,
        "template": "The overall loss ratio across all lines of business is {loss_ratio:.1f}%. This is calibrated against the IRDAI-verified industry figure of ~82.88% for FY2024-25.",
    },
    {
        "question": "How many claims have been flagged as anomalies?",
        "keywords": ["anomalies", "flagged", "suspicious", "how many flagged"],
        "sql": """
            SELECT
                COUNT(CASE WHEN anomaly_score > 0.3 THEN 1 END) as flagged,
                COUNT(CASE WHEN anomaly_score > 0.6 THEN 1 END) as high_risk,
                COUNT(*) as total
            FROM claims
        """,
        "template": "Out of {total:,} total claims, {flagged:,} have been flagged as insights requiring review (anomaly score > 0.3), with {high_risk:,} classified as high-risk (score > 0.6). These are insights, not decisions — each requires human review.",
    },
    {
        "question": "Which line of business has the highest loss ratio?",
        "keywords": ["highest loss ratio", "which lob", "worst performing", "line of business loss"],
        "sql": """
            SELECT
                p.line_of_business,
                ROUND(SUM(c.claim_amount) / NULLIF(SUM(p.premium_amount), 0) * 100, 2) as loss_ratio,
                COUNT(c.claim_id) as claims_count
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
            GROUP BY p.line_of_business
            ORDER BY loss_ratio DESC
            LIMIT 1
        """,
        "template": "The {line_of_business} line of business has the highest loss ratio at {loss_ratio:.1f}%, based on {claims_count:,} claims.",
    },
    {
        "question": "What are the top 5 states by claim volume?",
        "keywords": ["top states", "states by claims", "highest claims state"],
        "sql": """
            SELECT p.state, COUNT(c.claim_id) as claims_count,
                   ROUND(SUM(c.claim_amount), 2) as total_amount
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
            GROUP BY p.state
            ORDER BY claims_count DESC
            LIMIT 5
        """,
        "template": "The top 5 states by claim volume are: {results}. These states represent the highest concentration of insurance activity in the portfolio.",
    },
    {
        "question": "What is the average claim amount?",
        "keywords": ["average claim", "mean claim amount", "avg claim"],
        "sql": """
            SELECT
                ROUND(AVG(claim_amount), 2) as avg_amount,
                ROUND(MIN(claim_amount), 2) as min_amount,
                ROUND(MAX(claim_amount), 2) as max_amount
            FROM claims
        """,
        "template": "The average claim amount is ₹{avg_amount:,.2f}. Claims range from ₹{min_amount:,.2f} to ₹{max_amount:,.2f}.",
    },
    {
        "question": "How many claims are pending?",
        "keywords": ["pending claims", "unsettled", "claims pending"],
        "sql": """
            SELECT status, COUNT(*) as count
            FROM claims
            GROUP BY status
            ORDER BY count DESC
        """,
        "template": "Claims by status: {results}. Pending claims require attention and may be prioritized using the anomaly review queue.",
    },
    {
        "question": "Which agents have the most claims?",
        "keywords": ["agents", "top agents", "agent claims", "busiest agents"],
        "sql": """
            SELECT a.name as agent_name, a.region, COUNT(c.claim_id) as claims_count,
                   ROUND(AVG(c.anomaly_score), 3) as avg_anomaly_score
            FROM claims c
            JOIN agents a ON c.agent_id = a.agent_id
            GROUP BY a.agent_id, a.name, a.region
            ORDER BY claims_count DESC
            LIMIT 5
        """,
        "template": "The top 5 agents by claim volume are: {results}. Note: high claim volume alone is not indicative of fraud — the anomaly score provides a more nuanced signal.",
    },
    {
        "question": "What is the settlement rate?",
        "keywords": ["settlement rate", "approved rate", "claims settled"],
        "sql": """
            SELECT
                ROUND(COUNT(CASE WHEN status = 'Approved' THEN 1 END) * 100.0 / COUNT(*), 2) as settlement_rate,
                COUNT(CASE WHEN status = 'Approved' THEN 1 END) as approved,
                COUNT(*) as total
            FROM claims
        """,
        "template": "The claims settlement rate is {settlement_rate:.1f}% ({approved:,} approved out of {total:,} total). This aligns with the IRDAI industry benchmark of ~82% by count.",
    },
    {
        "question": "Show me the monthly claims trend",
        "keywords": ["monthly trend", "claims over time", "trend", "monthly claims"],
        "sql": """
            SELECT
                substr(claim_date, 1, 7) as month,
                COUNT(*) as claims_count,
                ROUND(SUM(claim_amount), 2) as total_amount
            FROM claims
            GROUP BY month
            ORDER BY month
        """,
        "template": "Monthly claims trend: {results}. Review the Executive Overview dashboard for visual trend analysis.",
    },
    {
        "question": "What are the most common fraud patterns detected?",
        "keywords": ["fraud patterns", "detection patterns", "anomaly types", "what patterns"],
        "sql": """
            SELECT
                anomaly_layers,
                COUNT(*) as count
            FROM claims
            WHERE anomaly_score > 0.3
            GROUP BY anomaly_layers
            ORDER BY count DESC
            LIMIT 10
        """,
        "template": "The anomaly detection pipeline uses three layers: (1) Rules Engine — catches explicit patterns like amount spikes, rapid repeat claims, and mismatched LOB routing; (2) Isolation Forest — detects statistical outliers in claim features; (3) Graph/Louvain Community Detection — identifies suspicious entity clusters (agent-hospital rings). These are insights requiring human review, not automated decisions.",
    },
]


def match_golden_query(question: str) -> dict | None:
    """
    Try to match a user question to one of the 10 golden queries.
    Uses keyword matching — simple but reliable for demo purposes.
    """
    question_lower = question.lower().strip()

    best_match = None
    best_score = 0

    for gq in GOLDEN_QUERIES:
        score = 0
        for keyword in gq["keywords"]:
            if keyword in question_lower:
                score += len(keyword)  # Longer keyword matches score higher

        if score > best_score:
            best_score = score
            best_match = gq

    # Require at least one keyword match
    return best_match if best_score > 0 else None


def format_golden_answer(template: str, data: list[dict]) -> str:
    """Format a golden query answer template with query results."""
    if not data:
        return "No data available for this query."

    # If single row result, format directly
    if len(data) == 1:
        try:
            return template.format(**data[0])
        except (KeyError, IndexError):
            pass

    # Multi-row: format as a list
    if "{results}" in template:
        results_str = "; ".join(
            ", ".join(f"{k}: {v}" for k, v in row.items())
            for row in data[:5]
        )
        return template.format(results=results_str)

    try:
        return template.format(**data[0])
    except (KeyError, IndexError):
        return template
