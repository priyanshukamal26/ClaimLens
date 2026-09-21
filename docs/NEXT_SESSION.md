# NEXT_SESSION.md

## Current state
Documentation architecture generated (this docs/ set). No build-status source material was available to this pass — actual implementation state is unknown and must be established at the start of the next session.

## What was completed recently
- PS-compliance review (2026-09-21)
- Full dataset/technical/regulatory verification pass (2026-09-21)
- This documentation system, generated from the above two artifacts (2026-09-22)
- Dashboard visual concept (UI_UX_DESIGN_SYSTEM.md + published artifact) — see below

## Current blocking issues
See [KNOWN_ISSUES_RISKS.md](./KNOWN_ISSUES_RISKS.md), especially items A (time), C (AWS account risk), and G (unconfirmed dataset table).

## Immediate next task
Run the **Hour-0 checklist** in [PROJECT_TRACK.md](./PROJECT_TRACK.md) in full before any feature work:
1. Confirm current Gemini model ID in-console
2. Confirm AWS account status
3. Grant both Lambda invoke permissions on every Function URL
4. Open and verify the balajiadithya Excel sheet names
5. Lock dataset licenses
6. Reconcile PMFBY state/district names
7. Get explicit team sign-off on Cut Level 1 as the active target

## Next 3–10 tasks (after Hour-0)
1. Confirm real build status and overwrite every `STATUS UNKNOWN` in PROJECT_TRACK.md
2. If the original 697-line plan is available, supply it so PAGES.md, API.md, and DATABASE.md can be generated with real content instead of `PENDING`
3. Build/verify synthetic data generator against confirmed dataset schemas
4. Build/verify three-layer anomaly detection pipeline
5. Build/verify Ask ClaimLens agent chain against the reconfirmed Gemini model ID
6. Test the LLM fallback chain end-to-end (simulate Groq quota exhaustion)
7. Test the 25-case hostile-query suite against the SQL guard
8. Deploy to AWS and run the production verification checklist in DEPLOYMENT.md
9. Rehearse the demo against golden queries only (in case live LLM calls are needed as backup, not primary)

## Files likely to be touched next
PROJECT_TRACK.md (constantly), plus whichever of API.md / DATABASE.md / PAGES.md get created once the original plan is supplied.

## Things the next agent must inspect before changing
Actual repository state (if one exists) — this documentation set was generated without visibility into any codebase.

## Things the next agent must NOT redo
- The PS-compliance review and verification pass — their findings are CONFIRMED in HISTORY.md and should be trusted, not re-derived, unless something material has changed
- The Cut Level 1 decision — treat as ACCEPTED per ADR-005 unless the team explicitly overrides it

## Suggested first command/action
Read MASTER.md's warning block, then execute PROJECT_TRACK.md's Hour-0 checklist.

## Ready-to-copy next-session prompt

```
You are continuing work on ClaimLens Nexus (Insurance Insight Nexus, Track 2).

First read:
- docs/MASTER.md
- docs/PROJECT_TRACK.md
- docs/NEXT_SESSION.md
- docs/KNOWN_ISSUES_RISKS.md

Do not restart or redesign already-completed planning work (PS-compliance review,
dataset verification, Cut Level decision) without a documented reason in HISTORY.md.

Current state:
Documentation-only pass complete. Build status unknown. Submission is time-critical
per the source material's own schedule.

Current task:
Execute the Hour-0 checklist in PROJECT_TRACK.md, then report real build status
so PROJECT_TRACK.md's task hierarchy can be updated from STATUS UNKNOWN to real values.

Acceptance criteria:
Every Hour-0 checklist item is either DONE or explicitly BLOCKED with a reason.

Relevant files:
docs/DEPLOYMENT.md (Lambda gotcha), docs/AI_ML.md (Gemini model lifecycle),
docs/DATA.md (dataset verification items G/H).

Constraints:
Cut Level 1 is the active target (ADR-005) unless the team explicitly overrides it
in a new HISTORY.md entry.

After completing the work:
1. Test whatever was implemented.
2. Update docs/PROJECT_TRACK.md with timestamps.
3. Update docs/HISTORY.md.
4. Update any documentation affected by the changes.
5. Update docs/NEXT_SESSION.md.
6. Generate the prompt for the following session.
```
