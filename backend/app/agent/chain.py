"""
ClaimLens Nexus — Agent Chain Orchestrator

Full pipeline: router → planner → SQL writer → guard → verifier → narrator
Per ARCHITECTURE.md: this is the Ask ClaimLens feature (FR-004).

Per ADR-004: every answer is badged INSIGHT, never DECISION.
"""

from app.agent.golden_queries import match_golden_query, format_golden_answer
from app.agent.guard import validate_sql, SQLGuardError
from app.agent.llm_client import call_llm
from app.database import execute_analytics_query


# Schema description for the SQL writer
SCHEMA_PROMPT = """You are a SQL expert working with an insurance analytics database.
The database has these tables:

1. policies (policy_id TEXT PK, policyholder_name TEXT, state TEXT, line_of_business TEXT,
   insurer TEXT, premium_amount REAL, start_date TEXT, end_date TEXT, status TEXT)

2. claims (claim_id TEXT PK, policy_id TEXT FK, claim_amount REAL, claim_date TEXT,
   settlement_amount REAL, settlement_date TEXT, status TEXT, hospital_id TEXT,
   garage_id TEXT, agent_id TEXT, claim_type TEXT, fraud_flag INT, anomaly_score REAL,
   anomaly_layers TEXT)

3. hospitals (hospital_id TEXT PK, name TEXT, city TEXT, state TEXT, tpa_network TEXT, bed_count INT)

4. garages (garage_id TEXT PK, name TEXT, city TEXT, state TEXT, service_type TEXT)

5. agents (agent_id TEXT PK, name TEXT, region TEXT, commission_rate REAL, active_policies_count INT)

6. decisions (decision_id TEXT PK, claim_id TEXT FK, insight_type TEXT, decision_type TEXT,
   decided_by TEXT, decided_at TEXT, rationale TEXT)

Lines of business: Health, Motor, Fire, Marine, Miscellaneous
Claim types: Cashless, Reimbursement, Third-Party, Own Damage
Claim statuses: Pending, Approved, Rejected, Under Investigation
Policy statuses: Active, Expired, Cancelled

Use DuckDB SQL dialect. Dates are stored as 'YYYY-MM-DD' strings, so use substr(date_col, 1, 7) to group by month.
Return ONLY the SQL query, nothing else. No markdown, no explanation."""


NARRATOR_PROMPT = """You are a narrator for an insurance analytics platform called ClaimLens Nexus.
Given a user's question and query results, provide a clear, professional answer.

CRITICAL RULES:
1. You surface INSIGHTS, never DECISIONS. Always frame findings as observations requiring human review.
2. Never say "the system decided" or "we recommend" — say "the data shows" or "this pattern suggests".
3. Be specific with numbers and use Indian currency (₹) formatting.
4. Keep answers concise (2-4 sentences for simple queries, up to a short paragraph for complex ones).
5. If the data shows anomalies, note they are flagged for review, not confirmed as fraud."""


async def run_agent_chain(question: str) -> dict:
    """
    Run the full Ask ClaimLens agent chain.

    Steps:
    1. Router: check if it matches a golden query first
    2. Planner: decompose the question (via LLM)
    3. SQL Writer: generate SQL (via LLM)
    4. Guard: validate SQL through sqlglot allowlist
    5. Execute: run against read-only DuckDB
    6. Verifier: check results are reasonable
    7. Narrator: turn results into plain language (via LLM)
    """

    # Step 1: Router — try golden queries first (deterministic, no LLM needed)
    golden = match_golden_query(question)
    if golden:
        try:
            results = execute_analytics_query(golden["sql"])
            answer = format_golden_answer(golden["template"], results)
            return {
                "answer": answer,
                "sql_used": golden["sql"].strip(),
                "source": "golden_query",
                "is_insight": True,
            }
        except Exception as e:
            print(f"Golden query execution failed: {e}")
            # Fall through to LLM path

    # Steps 2-3: Planner + SQL Writer (combined in one LLM call for efficiency)
    sql_prompt = f"""Question: {question}

Generate a single DuckDB SQL SELECT query to answer this question about the insurance data.
Return ONLY the raw SQL, no markdown formatting, no backticks, no explanation."""

    sql_response, sql_source = await call_llm(sql_prompt, SCHEMA_PROMPT)

    # If LLM failed (fell through to template), use a generic response
    if sql_source == "template" or not sql_response.strip():
        return _template_fallback(question)

    # Clean the SQL response
    sql = _clean_sql(sql_response)

    # Step 4: Guard — validate through sqlglot allowlist
    try:
        validated_sql = validate_sql(sql)
    except SQLGuardError as e:
        return {
            "answer": f"I wasn't able to safely process that query. The SQL guard flagged: {e}. Please try rephrasing your question.",
            "sql_used": sql,
            "source": f"guard_blocked ({sql_source})",
            "is_insight": True,
        }

    # Step 5: Execute against read-only DuckDB
    try:
        results = execute_analytics_query(validated_sql)
    except Exception as e:
        return {
            "answer": f"The query executed but encountered an error: {str(e)[:200]}. Please try rephrasing.",
            "sql_used": validated_sql,
            "source": f"execution_error ({sql_source})",
            "is_insight": True,
        }

    # Step 6: Verifier — basic result validation
    if not results:
        return {
            "answer": "The query returned no results. This might mean the data doesn't contain matching records, or the question needs to be rephrased.",
            "sql_used": validated_sql,
            "source": sql_source,
            "is_insight": True,
        }

    # Step 7: Narrator — turn results into natural language
    narrator_prompt = f"""Question: {question}

SQL used: {validated_sql}

Results (first 10 rows):
{_format_results_for_narrator(results[:10])}

Provide a clear, professional answer based on these results."""

    narration, narrator_source = await call_llm(narrator_prompt, NARRATOR_PROMPT)

    if narrator_source == "template" or not narration.strip():
        # Fallback: format results directly
        narration = _format_results_as_answer(question, results)

    return {
        "answer": narration,
        "sql_used": validated_sql,
        "source": sql_source,
        "is_insight": True,
    }


def _clean_sql(raw: str) -> str:
    """Clean LLM-generated SQL response."""
    sql = raw.strip()
    # Remove markdown code fences
    if sql.startswith("```"):
        lines = sql.split("\n")
        sql = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    sql = sql.strip("`").strip()
    # Remove trailing semicolons (sqlglot handles this)
    if sql.endswith(";"):
        sql = sql[:-1].strip()
    return sql


def _format_results_for_narrator(results: list[dict]) -> str:
    """Format query results as a string for the narrator prompt."""
    if not results:
        return "No results"
    lines = []
    for i, row in enumerate(results):
        lines.append(f"Row {i+1}: {row}")
    return "\n".join(lines)


def _format_results_as_answer(question: str, results: list[dict]) -> str:
    """Format results directly as a plain-text answer (no LLM narrator)."""
    if len(results) == 1:
        row = results[0]
        parts = [f"{k}: {v}" for k, v in row.items() if v is not None]
        return f"Based on the data: {', '.join(parts)}."

    lines = [f"The query returned {len(results)} results:"]
    for row in results[:5]:
        parts = [f"{k}: {v}" for k, v in row.items() if v is not None]
        lines.append(f"  • {', '.join(parts)}")
    if len(results) > 5:
        lines.append(f"  ... and {len(results) - 5} more rows.")
    return "\n".join(lines)


def _template_fallback(question: str) -> dict:
    """Static template fallback when no LLM is available."""
    return {
        "answer": (
            "I'm currently operating in offline mode without access to the AI language model. "
            "Try one of these pre-validated questions: "
            "'What is the overall loss ratio?', "
            "'How many claims have been flagged as anomalies?', "
            "'Which line of business has the highest loss ratio?', "
            "'What are the top 5 states by claim volume?', "
            "'What is the average claim amount?', "
            "'How many claims are pending?', "
            "'Which agents have the most claims?', "
            "'What is the settlement rate?', "
            "'Show me the monthly claims trend', or "
            "'What are the most common fraud patterns detected?'"
        ),
        "sql_used": None,
        "source": "template",
        "is_insight": True,
    }
