# ERRORS_EDGE_CASES.md — Error Handling & Edge Cases

ClaimLens Nexus anticipates and handles several critical edge cases gracefully, particularly around LLM interactions and data loading.

## 1. LLM API Failures (Rate Limits, Downtime)
**Scenario**: The primary LLM provider (Groq) throws a 429 Rate Limit or 503 Service Unavailable error.
**Handling**: The `Ask ClaimLens` agent chain implements a 4-stage fallback (`app/agent/chain.py`):
1. Groq (Primary)
2. Gemini (Secondary)
3. Semantic Cache (Local lookup of similar past questions)
4. Template Fallback (Pre-canned safe responses for Golden Queries)
The frontend displays the source of the answer so the user knows if it was a live model or a fallback.

## 2. Hostile SQL Generation
**Scenario**: The LLM misinterprets a prompt (or suffers prompt injection) and generates destructive SQL (`DROP TABLE`, `UPDATE`).
**Handling**: The `sqlglot` guard (`app/agent/guard.py`) intercepts the SQL before execution. It parses the AST, identifies the destructive operation, and raises a `SQLGuardError`.
The backend catches this error, logs the attempt, and returns a sanitized 400 Bad Request to the frontend: *"Generated SQL failed security validation."*

## 3. Database Concurrency (DuckDB)
**Scenario**: Two users attempt to query the analytics database while it is being reloaded after an anomaly detection run.
**Handling**: DuckDB is designed for single-process write access. The backend manages this via explicit connection scoping and read-only mode (`read_only=True`). The `execute_analytics_query` function handles connection pooling and transient locks.

## 4. Unrecognized Entities in NL-to-SQL
**Scenario**: The user asks "Show me claims for Hospital XYZ" but Hospital XYZ does not exist in the synthetic dataset.
**Handling**: The LLM will likely generate valid SQL looking for that string. The query will return 0 rows. The Verifier step in the agent chain detects the empty result set and instructs the Narrator to politely inform the user that no matching records were found, rather than hallucinating data.

## 5. Missing Environment Variables
**Scenario**: The user boots the app without setting `GROQ_API_KEY`.
**Handling**: The backend falls back gracefully. Standard analytics and anomaly queues continue to function normally. The `Ask ClaimLens` feature will immediately trigger the fallback chain, utilizing the Template system for Golden Queries without crashing the server.

## 6. Frontend Loading States
**Scenario**: Complex DuckDB queries take >1 second to return.
**Handling**: All frontend components (`ExecutiveOverview`, `ReviewQueue`) implement localized loading spinners or skeleton screens. If an API call fails completely, the component catches the error and displays a localized fallback (e.g., the IRDAI panel simply won't render if the external API is unreachable, but the rest of the dashboard remains functional).
