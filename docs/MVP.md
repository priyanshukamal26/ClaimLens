# MVP.md — Scope Tiers

The original plan defines its own Cut Levels for exactly this purpose. This file makes the active tier explicit and strict, per the universal template's "MVP-first rule": no feature is added because it looks impressive.

## Recommended active target: Cut Level 1

> Source material's own build schedule assumed ~22 hours of focused, parallel build time from T+3, with submission on the same day this documentation was generated. Given that, the PS-compliance review's recommendation is to **decide Cut Level 1 as the real target now**, not treat it as an emergency fallback discovered at T+14.

### Full scope (Cut Level 0 — only if measurably ahead of schedule)
- Executive Overview (trends by line & state)
- Full three-layer anomaly detection incl. held-out pattern eval (P4)
- Ranked review queue + gain chart + Morning Brief
- Ask ClaimLens full agent chain + 10 golden queries
- Insight vs Decision UI + Decision Log
- Analytics page
- District-level PMFBY panel
- IRDAI/PMFBY integration panels
- Full 8-page responsive frontend
- Full AWS deployment + CI/CD

### Cut Level 1 (recommended active baseline)
Drops from Cut Level 0:
- ❌ Analytics page
- ❌ Optional/secondary anomaly baseline model
- ❌ District-level PMFBY panel (also blocked on state/district reconciliation — see KNOWN_ISSUES_RISKS.md)

Keeps everything else, including the standout differentiators (held-out pattern eval, insight/decision separation, SQL defense-in-depth) — these should be protected from cuts before anything else is dropped, since they carry the Innovation/Business Value judging weight.

### Cut Level 2 (stretch only, PENDING exact content from original plan)
Exact item list: `PENDING — requires original plan`. Per the PS-compliance review, Cut Level 2 items should only be attempted if ahead of schedule by roughly T+10, not decided reactively under time pressure.

### Cut Level 3 (PENDING exact content from original plan)
`PENDING — requires original plan`.

## MVP objective
Demonstrate cloud-native trend analysis, unusual-pattern detection, and natural-language querying over synthetic Indian insurance data, with an explicit and enforced insight-vs-decision boundary, deployed on AWS within free-tier limits.

## MVP user journey (ASSUMED shape, based on named features — exact flow PENDING original plan)
1. Land on Executive Overview → see trend summary
2. See ranked review queue of flagged claims (INSIGHT-badged)
3. Ask a natural-language question via Ask ClaimLens → get a narrated, SQL-transparent answer
4. Review Morning Brief for a synthesized daily summary
5. Any action taken on a flagged item routes to the Decision Log, not an automated resolution

## MVP pages (confirmed to exist by name; full inventory PENDING)
- Executive Overview
- Review queue / ranked queue view
- Ask ClaimLens (NL query interface)
- Decision Log

## MVP backend capabilities
- Trend aggregation queries (claims/premium/loss ratio by line & state, monthly)
- Three-layer anomaly scoring pipeline
- Guarded NL-to-SQL agent chain over read-only DuckDB
- Decision Log read/write

## MVP AI/ML capabilities
See [AI_ML.md](./AI_ML.md).

## MVP deployment
AWS: S3 + CloudFront (frontend), Lambda + API Gateway (backend), DynamoDB (data). See [DEPLOYMENT.md](./DEPLOYMENT.md).

## MVP success criteria
- Demo runs live in front of judges without breaking due to LLM rate limits (Demo Mode / cache / template fallback must actually function)
- Insight vs Decision distinction is visible and correct on every flagged item
- At least the 10 golden queries answer correctly and deterministically even if live LLM calls fail
- Deployed and reachable on AWS, not localhost, at demo time

## Out of scope for MVP
Anything under Cut Level 1's drop list above, plus anything not explicitly named in the PS or the source analyses.
