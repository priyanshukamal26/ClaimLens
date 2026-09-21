# AI_ML.md

## Ask ClaimLens agent chain
```
Steps:  router → planner → SQL writer → guard → verifier → narrator
Input:  natural-language question from user
Output: narrated answer + the SQL used, shown for transparency
```
- **Router:** classifies the query type / decides which downstream path handles it. Exact logic: `PENDING — requires original plan`.
- **Planner:** decomposes the question into a query plan.
- **SQL writer:** generates candidate SQL against the read-only DuckDB analytics layer.
- **Guard:** validates generated SQL through a sqlglot allowlist before execution — this is the primary SQL-injection defense layer.
- **Verifier:** checks the result before it's narrated (exact verification logic: `PENDING`).
- **Narrator:** turns the result into a plain-language answer.

## Deterministic fallback — 10 golden queries
A fixed set of pre-validated question/answer pairs that bypass the live LLM chain entirely. This is a deliberate hedge against LLM flakiness during a live demo, not a placeholder — treat it as load-bearing for the demo, and test it explicitly (see TESTING gap below).

## LLM provider chain and why it's 4 deep
```
1. Groq   (primary — fast inference)
2. Gemini (fallback)
3. Cache  (fallback — previously-served responses)
4. Static template / 10 golden queries (final fallback)
```
**Why this matters more than it looks:** free-tier rate limits are tight enough to plausibly exhaust mid-demo:
- **Groq free tier (verified 2026-09-21):** roughly 30 requests/minute and ~1,000 requests/day per model — varies by model (e.g. `llama-3.1-8b-instant` gets 14,400/day). Token-per-minute caps can bind before the request cap does.
- A few rounds of rehearsal plus live judge questions can plausibly burn a daily quota. **The Demo Mode / cache / template fallback must be tested end-to-end before the actual demo**, not assumed to work because it exists in the architecture.

## Gemini model lifecycle — re-verify before every build session
```
Gemini 1.5              DISCONTINUED (Sept 2025)
Gemini 2.0 Flash/Lite    SHUT DOWN (1 June 2026)
Gemini 2.5 (Flash/Lite/Pro)  Retirement announced, no earlier than 16 Oct 2026
Current GA (verified 2026-09-21): Gemini 3.1 Flash / Flash-Lite
```
**Do not hardcode a model ID from memory, from this document, or from the original plan.** Confirm the exact model ID in Google AI Studio at the start of the build session — this stack moves fast enough that "current" changes every few weeks.

## Anomaly detection — three layers
```
Layer 1: Rules engine           — interpretable, explicit fraud-indicator rules
Layer 2: Isolation Forest       — statistical outlier detection
Layer 3: Graph / Louvain communities — relational pattern detection across entities
```
Combined into a single anomaly score feeding the ranked review queue.

## Held-out fraud pattern (P4) — evaluation methodology
A pattern deliberately held out of the tuning process to test whether detection generalizes, rather than "we tuned on our own test set." PROPOSED beyond the PS's ask, but high-value — it directly defends against a judge asking whether precision/recall claims are circular. Exact methodology: `PENDING — requires original plan`.

## Validation / hallucination mitigation
- SQL guard (sqlglot allowlist) prevents unsafe generated SQL from executing
- Read-only DuckDB with external access disabled provides a second isolation layer
- Verifier step in the agent chain checks results before narration
- 25-case hostile-query test suite in CI exercises the guard against adversarial inputs (see TESTING gap — `PENDING` for exact test cases)

## Model limitations / failure cases (known)
- LLM rate-limit exhaustion mid-demo — mitigated by the 4-stage fallback chain, but only if tested
- Stale/retired Gemini model ID — hard failure unless reconfirmed at build time
- Any output implying a **decision** rather than an **insight** — this is a product-level failure, not just a technical one, and must be caught in UI review, not just backend logic

## PENDING — cannot be documented without the original plan
Exact router/verifier logic, exact prompt templates, exact P4 methodology, exact 25 hostile-query test cases, exact 10 golden queries.
