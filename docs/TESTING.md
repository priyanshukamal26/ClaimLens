# TESTING.md — Test Strategy & Coverage

## Core Strategy

ClaimLens Nexus relies heavily on the `pytest` framework for backend verification. Given the AI-driven nature of the application, our testing strategy prioritizes **Security** and **Deterministic Output**.

We do not currently write unit tests for the LLM output itself (as LLMs are non-deterministic), but we *do* rigorously test the guardrails surrounding the LLM.

## Security Testing (The SQL Guard)

The most critical test suite is `tests/test_guard.py`.

### Execution
```bash
cd backend
python -m pytest tests/test_guard.py -v
```

### Coverage
The suite executes 34 tests targeting `app/agent/guard.py`:

**25 Hostile Attack Vectors (True Negatives)**
The suite attempts to bypass the `sqlglot` guard using known SQL injection techniques. Every single one of these must raise a `SQLGuardError`:
1. `DROP TABLE`
2. Stacked statements (`SELECT ... ; DROP ...`)
3. `INSERT` / `UPDATE` / `DELETE`
4. `CREATE TABLE AS` / `ALTER TABLE`
5. `ATTACH DATABASE` / `DETACH DATABASE`
6. `PRAGMA`
7. System functions (`system()`, `read_csv()`)
8. Extensions (`INSTALL httpfs`)
9. Schema probing (`SELECT * FROM sqlite_master`)
10. Unallowed tables (`users`, `passwords`)
11. Denial of Service (`sleep()`, `pg_sleep()`)
12. Subquery mutations
13. Comment injection (`--`)
14. Malformed/Empty/Whitespace SQL
15. Exfiltration (`COPY TO`)
16. Config manipulation (`SET enable_external_access = true`)

**9 Legitimate Queries (True Positives)**
The suite verifies that valid, complex analytical queries (e.g., joins, aggregations, date grouping) pass through the guard unchanged without false positives.

## Continuous Integration (CI/CD)

All tests are automated via GitHub Actions (`.github/workflows/ci.yml`).

On every `push` or `pull_request` to `main`:
1. **Backend Job**: Installs Python 3.12, installs dependencies, and runs the `pytest` suite.
2. **Frontend Job**: Installs Node 20, runs `npm ci`, and executes `npx vite build` to ensure the frontend compiles without errors.

The build fails if any security test is bypassed or if the frontend fails to compile.
