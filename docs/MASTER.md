# MASTER.md — ClaimLens Nexus

## Project identity
```
Project Name:          ClaimLens Nexus
Track:                 Track 2 — "Insurance Insight Nexus" problem statement
Project Version:       1.0.0 (MVP Complete)
Documentation Version: 2.0 (Post-Implementation)
Current Project Phase: Integration & Polish (Phase 7)
Current Project Status: IMPLEMENTED — backend and frontend operational locally
Last Updated:          2026-09-22
```

## One-paragraph description
ClaimLens Nexus is a cloud-native (AWS) insurance analytics platform built for the "Insurance Insight Nexus" hackathon track. It ingests synthetic Indian insurance data (policies, claims, hospitals, garages, agents), surfaces claims/premium/loss-ratio trends, flags unusual patterns via a three-layer anomaly-detection stack (rule engine + Isolation Forest + graph/Louvain community detection), and lets users ask natural-language questions through a guarded, multi-step LLM agent pipeline. Its defining design principle — treated as a first-class UX constraint, not a disclaimer — is that the system surfaces **insights**, never **decisions**: every anomaly is badged INSIGHT, decisions live in a separate auditable Decision Log, and this distinction is enforced end-to-end in the UI copy and data model.

## Problem being solved
Insurance operations teams need faster, more legible ways to (a) see claims/premium/loss-ratio trends, (b) catch unusual claim patterns (fraud indicators) without hard-coding brittle rules, and (c) let non-technical stakeholders ask questions of the data in plain English — while keeping a clear line between "the system noticed X" and "a human decided Y," per the PS's explicit requirement.

## Goal / definition of success
A demoable, deployed-on-AWS system that a hackathon judge can (1) open, (2) see real trend/anomaly output on synthetic data, (3) ask a natural-language question of live in front of them, and (4) come away understanding that every flagged item is an insight requiring human sign-off, not an automated decision — all without the demo breaking due to an LLM rate limit or an AWS permissions gotcha.

## Current MVP scope
See [MVP.md](./MVP.md) for the full breakdown. Headline: the plan's own "Cut Level" system is the MVP lever. Given submission is **today**, this doc set treats **Cut Level 1** (drop Analytics page, optional baseline model, district panel) as the operating baseline, not an emergency fallback — see [PROJECT_TRACK.md](./PROJECT_TRACK.md).

## Explicitly excluded from MVP
- Analytics page (Cut Level 1)
- Optional/secondary anomaly baseline model (Cut Level 1)
- District-level PMFBY panel (Cut Level 1) — also blocked on state/district name reconciliation, see [KNOWN_ISSUES_RISKS.md](./KNOWN_ISSUES_RISKS.md)
- Anything not in the PS's stated scope (dashboards, analytics, anomaly detection, fraud indicators, NL exploration, AI summaries) — see [REQUIREMENTS.md](./REQUIREMENTS.md)

## Technology stack (summary — full detail in TECH_STACK.md)
- **Frontend:** React + Vite + Tailwind, responsive
- **Backend:** FastAPI on AWS Lambda
- **Database:** DynamoDB
- **Storage/CDN:** S3 + CloudFront
- **Anomaly detection:** rules engine + Isolation Forest + graph/Louvain community detection (three layers)
- **NL-to-SQL agent:** router → planner → SQL writer → guard → verifier → narrator, over read-only DuckDB, guarded with a sqlglot allowlist
- **LLM chain:** Groq (primary) → Gemini (fallback) → cache → static template (final fallback)
- **Deployment target:** AWS, free-tier ceilings tracked per service

## High-level architecture
See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full picture and a Mermaid diagram. In one line: Browser → CloudFront/S3 (React SPA) → API Gateway/Lambda (FastAPI) → DynamoDB + DuckDB (analytics layer) → external LLM APIs (Groq/Gemini) + external data panels (IRDAI/PMFBY).

## Documentation map

| File | Purpose | Read when |
|---|---|---|
| MASTER.md | Entry point, this file | Always, first |
| PROJECT_TRACK.md | Live execution tracker, Cut-Level decision, timestamped log | Every session |
| HISTORY.md | Permanent decision/verification history | Before changing any prior decision |
| REQUIREMENTS.md | PS requirement traceability matrix | Any feature work |
| MVP.md | Scope tiers (Full / Cut 1 / Cut 2 / Cut 3) | Scoping decisions |
| ARCHITECTURE.md | System architecture, data flow, diagrams | Backend/infra work |
| TECH_STACK.md | Stack choices, why, alternatives, limits | Any tech decision |
| DATA.md | Every dataset — verified availability, license, real fit | Any data-pipeline work |
| AI_ML.md | Agent pipeline, anomaly-detection layers, LLM fallback chain | AI/ML work |
| DECISIONS.md | ADRs for major architectural/technical choices | Before reversing a decision |
| DEPLOYMENT.md | AWS deployment plan, the Lambda 403 gotcha, build order | Deployment work |
| COST_PLAN.md | Free-tier ceilings and risk per service | Before enabling any paid-capable service |
| KNOWN_ISSUES_RISKS.md | Every open risk, blocker, and unresolved item | Every session, esp. before demo |
| UI_UX_DESIGN_SYSTEM.md | Visual design system (Wise-inspired) + dashboard concept | Frontend/design work |
| NEXT_SESSION.md | Current handoff state | Start of every session |

## Source-of-truth rules
- **PS requirement coverage** → REQUIREMENTS.md (table sourced verbatim from the PS-compliance review)
- **Dataset facts (existence, license, real schema)** → DATA.md (independently verified, not taken on faith from the original plan)
- **Regulatory/calibration figures** → DATA.md §Regulatory (verified against source as of 2026-09-21)
- **AWS/LLM technical facts** → DEPLOYMENT.md and AI_ML.md (verified as of 2026-09-21; re-verify LLM model IDs at build time — see warning below)
- **Anything not covered by the two source analyses** → `PENDING`, tracked as an open task in PROJECT_TRACK.md, never invented

## Current project state
```
Completed:    MVP Implementation (FastAPI, React, SQL Guard, CI/CD, Documentation)
In Progress:  AWS Deployment (Requires user credentials)
Blocked:      AWS Deployment (Pending manual deployment steps by user)
```

## Immediate next task
**Deploy to AWS** following the steps in [DEPLOYMENT.md](./DEPLOYMENT.md), and record the **Demo Video** for submission.

## Important warnings (do not accidentally break these)
1. **Lambda Function URL 403.** Grant both `lambda:InvokeFunctionUrl` AND `lambda:InvokeFunction` — a change from October 2025 that is still tripping teams. See DEPLOYMENT.md.
2. **Gemini model ID.** Do not hardcode any Gemini model name from memory or from this doc set. Gemini 1.5 is discontinued, Gemini 2.0 (Flash/Flash-Lite) was shut down 1 June 2026, and Gemini 2.5 has an announced retirement no earlier than **16 October 2026** — three weeks after today. Confirm the live GA model ID (as of the verification pass: Gemini 3.1 Flash/Flash-Lite) in Google AI Studio at the start of the build session. See AI_ML.md.
3. **Groq free-tier quota is load-bearing, not a nice-to-have.** ~30 req/min and roughly 1,000 req/day per model (varies by model). A few rehearsal rounds plus live judge Q&A can burn the daily quota. The Demo Mode / cache / template fallback chain must actually work before the demo, not just exist in the plan. See AI_ML.md and KNOWN_ISSUES_RISKS.md.
4. **Insight ≠ Decision is a hard product constraint, not a copy nit.** Every anomaly surfaced must carry an INSIGHT badge and route to the Decision Log rather than any UI element implying the system decided something. This is graded and is the plan's standout differentiator — see REQUIREMENTS.md and UI_UX_DESIGN_SYSTEM.md.
5. **Do not assume any dataset's undocumented columns exist.** In particular, the "TPA network hospital counts" claimed from the balajiadithya Kaggle file has not been confirmed present in that file — open it and check sheet names before writing code against it. See DATA.md.

## Project history location
[HISTORY.md](./HISTORY.md) — permanent, append-only.

## Session handoff procedure
Before making any significant change, read, in order: **MASTER.md → PROJECT_TRACK.md → NEXT_SESSION.md → HISTORY.md**, plus whichever topic file the task touches.
