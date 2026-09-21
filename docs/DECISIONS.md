# DECISIONS.md — Architecture / Technical Decision Records

## ADR-001 — Three-layer anomaly detection instead of a single method
```
Date:     PENDING (original plan)
Context:  PS requires "identify unusual patterns." A single rules-only or
          single ML-only approach has known blind spots.
Decision: Combine a rules engine, Isolation Forest, and graph/Louvain
          community detection into one anomaly score.
Alternatives: Rules-only (simpler, less defensible under judge Q&A);
          single ML model only (less interpretable).
Reason:   More rigorous than most hackathon entries attempt; each layer
          catches a different failure mode of the others.
Consequences: More implementation surface area and time cost — directly
          traded off against the Cut Level system if time runs short.
Status:   ACCEPTED
```

## ADR-002 — Guarded NL-to-SQL over a read-only DuckDB layer
```
Date:     PENDING (original plan)
Context:  PS requires natural-language question answering. LLM-generated
          SQL against a live database is a known injection/safety risk.
Decision: Read-only DuckDB, external access disabled, sqlglot allowlist
          guard on all generated SQL, 25-case hostile-query CI test suite.
Alternatives: Trust the LLM's SQL directly (rejected — unsafe);
          restrict to a fixed query library only (rejected — defeats the
          "ask anything" value proposition, though the 10 golden queries
          serve as a deterministic subset of exactly this).
Reason:   Defense-in-depth consistent with DuckDB's own published security
          guidance (confirmed in verification pass). Directly defends
          against a judge trying to break the system live.
Status:   ACCEPTED
```

## ADR-003 — 4-stage LLM fallback chain (Groq → Gemini → cache → template)
```
Date:     PENDING (original plan)
Context:  Free-tier LLM rate limits (Groq ~30 req/min, ~1,000 req/day per
          model) can plausibly be exhausted by rehearsal + live judge Q&A.
Decision: Chain Groq (primary) → Gemini (fallback) → response cache →
          static template / 10 golden queries as a final, always-available
          fallback.
Alternatives: Single provider only (rejected — single point of failure on
          the PS's most distinctive ask); no fallback (rejected).
Reason:   Makes the demo's hero feature resilient to a quota exhaustion
          event during the exact moment it matters most.
Consequences: Must be tested end-to-end before the demo — an untested
          fallback chain is not actually a mitigation. See
          KNOWN_ISSUES_RISKS.md item E.
Status:   ACCEPTED
```

## ADR-004 — Insight vs Decision as a first-class UI/data constraint
```
Date:     PENDING (original plan)
Context:  PS explicitly requires that analytical insights be clearly
          distinguished from final business decisions.
Decision: Every anomaly surfaced is badged INSIGHT; a separate Decision
          Log records human decisions; banner copy on every alert
          reinforces the distinction.
Alternatives: Treat this as a disclaimer/footnote (rejected — the PS-
          compliance review identifies this as the standout differentiator
          precisely because it was NOT treated this way).
Reason:   Directly answers the PS's most specific and most gradeable line;
          also the single feature the PS-compliance review flags as most
          worth protecting from Cut Level trims.
Status:   ACCEPTED — protect from scope cuts
```

## ADR-005 — Cut Level 1 as the active build target (not emergency fallback)
```
Date:     2026-09-22 (this documentation pass)
Context:  Source material's own schedule assumed ~22 hours from T+3, with
          submission the same day this documentation was generated.
Decision: Treat Cut Level 1 (drop Analytics page, optional baseline model,
          district panel) as the real target from the start of the
          session, not a fallback discovered under panic at T+14.
Alternatives: Build toward full scope and cut reactively if behind
          (rejected by the PS-compliance review as poor risk management
          given the team's likely 1-2 effective engineers).
Reason:   Pass/fail blockers (AWS account, dataset licensing) don't scale
          down gracefully the way frontend polish does — front-loading
          them and accepting a smaller confirmed scope beats a larger
          scope finished late or broken.
Status:   PROPOSED — requires explicit team confirmation (Hour-0 checklist
          item H0.7 in PROJECT_TRACK.md)
```
