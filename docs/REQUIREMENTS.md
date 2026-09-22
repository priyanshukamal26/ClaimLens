# REQUIREMENTS.md

Requirements below are sourced from the PS-compliance review's line-by-line comparison against the "Insurance Insight Nexus" (Track 2) problem statement. See [HISTORY.md](./HISTORY.md) for provenance and [SOURCE_REQUIREMENTS] note at the bottom.

## PS requirement traceability matrix

| ID | PS requirement | Status | Feature / implementation |
|---|---|---|---|
| FR-001 | Cloud-native platform, sample insurance data | CONFIRMED — Strong | S3/CloudFront/Lambda/DynamoDB + ingestion pipeline for policies, claims, hospitals, garages, agents |
| FR-002 | Analyze trends | CONFIRMED | Executive Overview: monthly claims/premium/loss ratio by line of business & state |
| FR-003 | Identify unusual patterns | CONFIRMED — Strong | Three-layer detection: rules engine + Isolation Forest + graph/Louvain community detection |
| FR-004 | Ask natural-language questions | CONFIRMED — Strong | "Ask ClaimLens" pipeline: router → planner → SQL writer → guard → verifier → narrator, with 10 golden queries as deterministic fallback |
| FR-005 | Faster decision-making | CONFIRMED | Ranked review queue + gain chart + Morning Brief |
| FR-006 | Synthetic data; insights ≠ decisions must be clearly distinguished | CONFIRMED — Standout feature | INSIGHT/DECISION badges, separate Decision Log, banner copy on every alert — first-class design constraint, not a disclaimer |
| FR-007 | Suggested scope: dashboards, analytics, anomaly detection, fraud indicators, NL exploration, AI summaries | CONFIRMED — All present | Each has a named feature and named UI page |
| UX-001 | React frontend | CONFIRMED | React + Vite + Tailwind, responsive breakpoints specified |
| API-001 | Backend APIs | CONFIRMED | FastAPI on Lambda, 12 documented endpoints (see API.md) |
| FR-008 | AI/Agentic AI "used meaningfully" | CONFIRMED | Multi-step agent chain (planner→writer→guard→verifier→narrator) |
| DEP-001 | AWS deployment | CONFIRMED | Named services, free-tier ceilings specified per service — see COST_PLAN.md |
| FR-009 | External/sample data integrations | CONFIRMED | Real IRDAI/PMFBY aggregate panels alongside synthetic core — see DATA.md |
| DEL-001 | 6 deliverables: code, architecture doc, CI/CD, demo video, deck, deployment guide | CONFIRMED | All deliverables either generated or templated (see task.md and NEXT_SESSION.md) |
| DEL-002 | Judging criteria mapped: Innovation, Business Value, Tech, UI/UX, Presentation | CONFIRMED | Original plan §2.8 explicitly maps each criterion to specific features |
| LOG-001 | Team name, size, submission format | CONFIRMED | Captured in team submission portal |

## Requirements that exceed the PS ask (PROPOSED value-adds, not PS-mandated)
- **P4 — Held-out fraud pattern evaluation.** Evaluates whether detection generalizes rather than being tuned on its own test set. PROPOSED by the original plan; not required by the PS. High value for judge Q&A defensibility.
- **SEC-001 — SQL-injection defense in depth.** Read-only DuckDB + sqlglot allowlist + 25-case hostile-query CI suite. PROPOSED; not required by the PS, but directly defends the "responsible AI" angle a judge may probe live.
- **DOC-001 — Interview-prep document.** Anticipates technical judge questions (precision/recall circularity, dangerous-SQL prevention). PROPOSED, documentation-only, no engineering cost.

## Non-functional requirements (inferred from verified constraints — labeled ASSUMED where not explicit)
- **NFR-001 (CONFIRMED):** All AWS services must stay within free-tier ceilings — see COST_PLAN.md.
- **NFR-002 (CONFIRMED):** LLM calls must degrade gracefully under free-tier rate limits (Groq ~30 req/min / ~1,000 req/day per model, varies by model) without breaking the demo — see AI_ML.md.
- **NFR-003 (CONFIRMED):** Frontend is responsive across desktop, tablet, and mobile breakpoints using flexbox grids and custom CSS media queries.
- **NFR-004 (CONFIRMED):** Dataset licenses must be resolved before submission packaging, not left as an open checklist item — see DATA.md.

