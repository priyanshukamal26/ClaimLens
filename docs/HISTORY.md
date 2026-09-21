# HISTORY.md — Permanent Project History

Append-only. Never delete an entry; mark superseded entries `DEPRECATED` instead.

---

### 2026-09-21 — PS-compliance review performed
**Event:** Full line-by-line comparison of the ClaimLens Nexus plan (all 697 lines, including previously-truncated sections) against the "Insurance Insight Nexus" (Track 2) problem statement.
**Outcome:** Strong match — every stated PS requirement mapped to a named feature. Plan assessed as engaging with the PS's actual wording, not a generic template.
**Findings that exceed the PS ask:** held-out fraud pattern (P4) evaluation, SQL-injection defense-in-depth (read-only DuckDB + sqlglot allowlist + 25-case hostile-query CI suite), interview-prep document anticipating judge questions.
**Risks identified (see KNOWN_ISSUES_RISKS.md for current status):** time budget, single-point-of-failure team structure, AWS free-tier/account risk, deferred dataset licensing, LLM rate-limit dependency, scope-vs-differentiation trade-off under Cut Levels.
**Status:** CONFIRMED — this review's findings are treated as accurate source-of-truth pending re-validation against actual code.

### 2026-09-21 — Full source verification pass performed
**Event:** Independent, live verification of every dataset, dataset link, technical claim, and regulatory citation referenced in the plan.
**Outcome:** All six cited datasets exist at their given URLs — no dead or hallucinated links. All AWS Lambda limits confirmed current. The Lambda Function URL 403 permissions gotcha (October 2025 change) confirmed real and currently active. DuckDB security posture confirmed consistent with DuckDB's own guidance.
**Important update discovered during verification (not in the original plan):** Gemini's generation lifecycle has moved further than the plan assumed — Gemini 1.5 fully discontinued, Gemini 2.0 Flash/Flash-Lite shut down 1 June 2026, and even the replacement Gemini 2.5 generation has an announced retirement no earlier than 16 October 2026. Current GA models at verification time: Gemini 3.1 Flash / Flash-Lite. **Action required:** confirm the exact model ID in-console at build time; do not hardcode from any document, including this one.
**Regulatory update discovered:** the IRDAI Insurance Fraud Monitoring Framework Guidelines, 2025 (effective 1 April 2026) has been in force for ~6 months as of the verification date — stronger pitch material than "upcoming regulation" framing.
**Status:** CONFIRMED as of verification date (2026-09-21). Model-ID and account-status items are time-sensitive and must be re-checked, not assumed to still hold.

### 2026-09-22 — Documentation architecture generated
**Event:** This docs/ system was generated from the two entries above plus the universal documentation-template structure. The original full plan text was not available to this pass.
**Previous state:** Project knowledge existed only as two narrative analysis documents plus an un-ingested original plan referenced by section number.
**New state:** Structured, cross-linked documentation set under docs/, with every claim traceable to one of the two source analyses and every gap explicitly marked `PENDING`.
**Reason:** To create a persistent, agent-consumable source of truth per the universal template's own operating principles (separate fact from assumption, preserve history, never invent requirements).
**Impact:** API-level, DB-schema-level, and full page-inventory documentation could not be generated at this pass and are tracked as open tasks in PROJECT_TRACK.md rather than fabricated.
**Status:** ACTIVE — supersedes nothing; this is the first documentation pass for this project.

---

## Deprecated / superseded items

None recorded yet. When a decision changes, copy its original entry here, mark it `DEPRECATED`, and record the new decision in a fresh dated entry above (per MASTER.md source-of-truth rules).
