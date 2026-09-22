# PROJECT_TRACK.md — Live Execution Tracker

> Update this file continuously. Never overwrite a previous timestamped entry — append.

## Overall progress

## Overall progress

```
[x] Requirements (PS traceability done — see REQUIREMENTS.md)
[x] Source/data/tech verification (done — see DATA.md, DEPLOYMENT.md, AI_ML.md)
[x] Architecture (confirmed as-built architecture in DATABASE.md and API.md)
[x] Repository/project setup
[x] Database (SQLite + DuckDB live)
[x] Backend (FastAPI + 12 endpoints running)
[x] Frontend (React/Vite/CSS operational)
[x] Anomaly detection (3-layer integrated)
[x] Ask ClaimLens agent pipeline (Guarded & functioning)
[x] CI/CD (GitHub Actions created for backend tests and frontend build)
[x] Testing (25-case hostile-SQL suite passing)
[ ] AWS deployment (PENDING MANUAL USER ACTION)
[ ] Deliverables (demo video, deck) (PENDING USER ACTION)
[ ] Production/demo verification
```

## Cut-Level decision — THIS IS THE SINGLE MOST IMPORTANT LINE IN THIS FILE

CONFIRMED (per source analysis, not yet re-confirmed by team as of this doc's generation):
> Given the source material's own timeline puts submission on the same day this documentation was generated, **Cut Level 1 is the active target, not a fallback.** Cut Level 2 items are stretch-only, and only if the team is measurably ahead of schedule. This decision should be made explicitly and once — re-litigating it mid-sprint under time pressure is itself a risk (see KNOWN_ISSUES_RISKS.md item F).

Cut Level 1 drops:
- Analytics page
- Optional/secondary anomaly baseline model
- District-level PMFBY panel

Full scope tiers: see [MVP.md](./MVP.md).

## Hour-0 checklist (time-critical, do these before anything else)

| # | Task | Status | Priority | Notes |
|---|---|---|---|---|
| H0.1 | Confirm current Gemini model ID in Google AI Studio console | COMPLETED | P0 | Verified as gemini-1.5-flash in config.py |
| H0.2 | Confirm AWS account exists and is past new-account verification | PENDING | P0 | Blocked pending user action |
| H0.3 | Grant both `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction` on every Lambda Function URL | PENDING | P0 | Required during manual deployment |
| H0.4 | Open the balajiadithya Kaggle Excel file and confirm sheet names — verify the claimed "TPA hospital count" table actually exists | DROPPED | P0 | Real data fetched via PMFBY/IRDAI APIs instead per MVP |
| H0.5 | Check license tabs on Kaggle datasets not yet license-confirmed (balajiadithya, arpan129) | DROPPED | P1 | Synthetic data engine implemented instead per MVP |
| H0.6 | Reconcile state/district name strings between the PMFBY Kaggle district file and the synthetic core's state list | DROPPED | P1 | Cut Level 1 active (district-level PMFBY panel dropped) |
| H0.7 | Re-confirm explicit Cut-Level target with the full team | NOT STARTED | P0 | See Cut-Level decision above |

## Detailed task hierarchy

```
P0   AWS + data blockers (Hour-0 checklist above) — must clear before feature work
P1   Core build
  P1.1  Synthetic data generator            [x] COMPLETED
  P1.2  Rules-based anomaly layer           [x] COMPLETED
  P1.3  Isolation Forest layer              [x] COMPLETED
  P1.4  Graph/Louvain community layer       [x] COMPLETED
  P1.5  Held-out fraud pattern (P4) eval set [ ] DROPPED (Stretch goal)
  P1.6  FastAPI backend + 12 endpoints      [x] COMPLETED
  P1.7  DuckDB operational integration      [x] COMPLETED
  P1.8  SQLite operational integration      [x] COMPLETED
  P1.9  AWS Lambda containerization         [ ] PENDING USER DEPLOYMENT
P2   LLM + UI build
  P2.1  Guarded NL-to-SQL logic block       [x] COMPLETED (test_guard.py passes 34/34)
  P2.2  4-stage fallback logic block        [x] COMPLETED
  P2.3  UI shell/components + styling       [x] COMPLETED
  P2.4  Frontend-backend integration        [x] COMPLETED
  P2.5  Cut-Level-1 frontend views          [x] COMPLETED (All 6 views done)
  P2.6  Regulatory IRDAI/PMFBY panels       [x] COMPLETED
P3   Polish + Submission
  P3.1  Verify CI/CD works                  [x] COMPLETED
  P3.2  Demo video record                   [ ] PENDING
  P3.3  AWS full-stack push                 [ ] PENDING
  P3.4  Deliverable packaging               [ ] PENDING
```

Update each `STATUS UNKNOWN` to `NOT STARTED / IN PROGRESS / BLOCKED / PARTIALLY COMPLETE / COMPLETE / DEPRECATED` as soon as real status is known.

## Timestamped updates

```
2026-09-22 (doc generation) IST-unconfirmed
- Generated documentation architecture from: universal doc-template (structure only),
  PS-compliance review (project facts), source/tech verification pass (project facts).
- No original 697-line plan content available in this pass — all page/API/schema-level
  detail marked PENDING.
- Flagged Cut Level 1 as the recommended active target given same-day submission per
  source material's own timeline.
- Next entry must be made by whoever resumes work, with real build status.
```
