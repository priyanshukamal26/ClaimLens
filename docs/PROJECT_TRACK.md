# PROJECT_TRACK.md — Live Execution Tracker

> Update this file continuously. Never overwrite a previous timestamped entry — append.

## Overall progress

```
[x] Requirements (PS traceability done — see REQUIREMENTS.md)
[x] Source/data/tech verification (done — see DATA.md, DEPLOYMENT.md, AI_ML.md)
[ ] Architecture (concept-level done; no confirmed as-built architecture)
[ ] Repository/project setup — STATUS UNKNOWN
[ ] Database — STATUS UNKNOWN
[ ] Backend (FastAPI on Lambda) — STATUS UNKNOWN
[ ] Frontend (React/Vite/Tailwind) — STATUS UNKNOWN
[ ] Anomaly detection (3-layer) — STATUS UNKNOWN
[ ] Ask ClaimLens agent pipeline — STATUS UNKNOWN
[ ] AWS deployment — STATUS UNKNOWN, HIGH RISK (see below)
[ ] CI/CD — STATUS UNKNOWN
[ ] Testing (incl. 25-case hostile-SQL suite) — STATUS UNKNOWN
[ ] Deliverables (code, architecture doc, CI/CD, demo video, deck, deployment guide) — STATUS UNKNOWN
[ ] Production/demo verification — STATUS UNKNOWN
```

**Why so much is "STATUS UNKNOWN":** the source material available to this documentation pass is a planning-compliance review and a fact-verification pass, not a build log. The next session must overwrite every "STATUS UNKNOWN" line above with real status before doing anything else.

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
| H0.1 | Confirm current Gemini model ID in Google AI Studio console | NOT STARTED | P0 | Do not trust any model name from memory — see AI_ML.md |
| H0.2 | Confirm AWS account exists and is past new-account verification | NOT STARTED | P0 | New accounts can be flagged for manual review — plausible blocker, see KNOWN_ISSUES_RISKS.md item C |
| H0.3 | Grant both `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction` on every Lambda Function URL | NOT STARTED | P0 | The single highest-value warning in the source material — see DEPLOYMENT.md |
| H0.4 | Open the balajiadithya Kaggle Excel file and confirm sheet names — verify the claimed "TPA hospital count" table actually exists | NOT STARTED | P0 | Do not write ingestion code against an unconfirmed table — see DATA.md |
| H0.5 | Check license tabs on Kaggle datasets not yet license-confirmed (balajiadithya, arpan129) | NOT STARTED | P1 | Must be locked before packaging, not during final hours — see DATA.md |
| H0.6 | Reconcile state/district name strings between the PMFBY Kaggle district file and the synthetic core's state list | NOT STARTED | P1 | Budget a real hour; author-noted desync, not a 10-minute join — see DATA.md |
| H0.7 | Re-confirm explicit Cut-Level target with the full team | NOT STARTED | P0 | See Cut-Level decision above |

## Detailed task hierarchy

```
P0   AWS + data blockers (Hour-0 checklist above) — must clear before feature work
P1   Core build
  P1.1  Synthetic data generator            STATUS UNKNOWN
  P1.2  Rules-based anomaly layer            STATUS UNKNOWN
  P1.3  Isolation Forest layer               STATUS UNKNOWN
  P1.4  Graph/Louvain community layer        STATUS UNKNOWN
  P1.5  Held-out fraud pattern (P4) eval set STATUS UNKNOWN   [stretch beyond PS ask — do not cut before Cut-Level-1 items]
  P1.6  FastAPI backend + 12 endpoints       STATUS UNKNOWN   (endpoint list: PENDING — requires original plan)
  P1.7  React frontend (8 pages per PS-review) STATUS UNKNOWN (page inventory: PENDING — requires original plan)
  P1.8  Ask ClaimLens agent chain            STATUS UNKNOWN   (router→planner→SQL writer→guard→verifier→narrator)
  P1.9  10 golden queries deterministic fallback STATUS UNKNOWN
  P1.10 Insight vs Decision UI + Decision Log STATUS UNKNOWN  [standout differentiator — protect this from cuts]
P2   Integrations
  P2.1  IRDAI/PMFBY panels                   STATUS UNKNOWN
P3   Hardening
  P3.1  sqlglot allowlist + read-only DuckDB  STATUS UNKNOWN
  P3.2  25-case hostile-query CI test suite   STATUS UNKNOWN
P4   Deployment
  P4.1  AWS account + IAM setup               STATUS UNKNOWN
  P4.2  S3/CloudFront frontend hosting         STATUS UNKNOWN
  P4.3  Lambda/API Gateway backend             STATUS UNKNOWN
  P4.4  DynamoDB provisioning                  STATUS UNKNOWN
  P4.5  CI/CD pipeline                         STATUS UNKNOWN
P5   Deliverables
  P5.1  Architecture doc     STATUS UNKNOWN
  P5.2  Demo video           STATUS UNKNOWN
  P5.3  Deck                 STATUS UNKNOWN
  P5.4  Deployment guide     STATUS UNKNOWN
  P5.5  Interview-prep doc   STATUS UNKNOWN
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
