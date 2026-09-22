# AUTH_SECURITY.md — Security Posture

ClaimLens Nexus takes security extremely seriously, particularly because it features an LLM capable of generating SQL that executes against a database. We employ a defense-in-depth strategy.

## 1. Natural Language to SQL Security (SEC-001)

The most critical security risk in the application is the `Ask ClaimLens` feature, where an LLM translates natural language into SQL.

**The Threat:** An attacker could use prompt injection to trick the LLM into generating destructive SQL (e.g., `DROP TABLE`, `DELETE FROM`, or data exfiltration via `httpfs`).

**The Defense (sqlglot Guard):**
We do NOT trust the LLM output. Before any LLM-generated SQL is executed, it passes through `app/agent/guard.py`:
1. **AST Parsing**: The SQL string is parsed into an Abstract Syntax Tree (AST) using `sqlglot`.
2. **Statement Type Validation**: The AST root node MUST be a `SELECT` statement. `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, etc., are instantly rejected.
3. **Table Allowlisting**: The AST is traversed to find all referenced tables. Every table MUST belong to a strict allowlist (`policies`, `claims`, `hospitals`, `garages`, `agents`, `decisions`). If the LLM tries to query `sqlite_master` or `users`, the query is rejected.
4. **Function Denylisting**: The AST is traversed to find all function calls. Dangerous functions (e.g., `system()`, `read_csv()`, `pg_sleep()`) are blocked.
5. **No Stacked Queries**: If `sqlglot` parses multiple statements (separated by `;`), the query is rejected.

*Verification*: This guard is enforced by a 25-case hostile test suite (`tests/test_guard.py`) that runs on every CI/CD pipeline execution.

## 2. Database Layer Security

**Dual-Database Isolation:**
- **DuckDB (Analytics)**: The LLM only ever executes queries against the DuckDB instance. This database is opened in `read_only=True` mode. Furthermore, we explicitly execute `SET enable_external_access = false;` upon connection to prevent DuckDB from reading or writing local files or making HTTP requests.
- **SQLite (Operational)**: The operational database holding the Decision Log is NEVER exposed to the LLM. It is strictly accessed via parameterized queries in the FastAPI routers (e.g., `decisions.py`), preventing standard SQL injection.

## 3. Data Privacy

- **Synthetic Data**: The core dataset (policies, claims) is entirely synthetic, generated dynamically upon first boot. No real PII/PHI exists in the operational store.
- **LLM Data Transmission**: When sending schema context to Groq/Gemini, we ONLY send the table schemas (column names and types). We NEVER send row data to the LLM.

## 4. Authentication (Mocked for MVP)

- Currently, authentication is mocked. In a production deployment, the FastAPI backend would implement OAuth2 + JWT (e.g., Azure AD, Auth0), and the React frontend would use a protected route wrapper.
- The `decided_by` field in the Decision Log is currently hardcoded to "Reviewer". In production, this would be extracted from the authenticated user's JWT payload.
