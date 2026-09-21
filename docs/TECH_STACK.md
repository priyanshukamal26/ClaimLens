# TECH_STACK.md

For each entry: what/why/alternatives are drawn from the source material where stated; free-tier notes are from the independent verification pass (verified 2026-09-21) and must be re-checked at build time since these ecosystems move fast.

## Frontend
```
Technology:   React + Vite + Tailwind CSS
Purpose:      Responsive SPA, hackathon frontend
Why chosen:   PENDING — requires original plan (rationale not in source material)
Free tier:    Vite/React/Tailwind have no usage costs themselves — cost lives in hosting (see below)
```

## Backend
```
Technology:   FastAPI on AWS Lambda
Purpose:      API layer, agent orchestration
Why chosen:   PENDING — requires original plan
Free tier:    See Lambda limits below — confirmed current as of 2026-09-21:
              250 MB unzipped package, 50 MB zipped, 6 MB sync response limit,
              15-minute max timeout, 1,769 MB memory = 1 vCPU
```

## Database
```
Technology:   DynamoDB
Purpose:      Application/decision-log data
Why chosen:   PENDING — requires original plan
Free tier:    Not independently re-verified in this pass — verify DynamoDB free-tier
              limits at build time (AWS free-tier terms change)
```

## Analytics layer
```
Technology:   DuckDB (read-only)
Purpose:      Backing store for NL-to-SQL agent queries
Why chosen:   Read-only, embeddable, and per DuckDB's own published guidance,
              a currently-recommended pattern for sandboxing untrusted SQL —
              confirmed consistent with that guidance in the verification pass
Limitations:  Requires explicit hardening (external access disabled) — this is
              already the plan's design, not an added recommendation
```

## Storage / CDN
```
Technology:   S3 + CloudFront
Purpose:      Frontend hosting, static assets
Free tier:    Standard AWS free-tier ceilings apply — see COST_PLAN.md
```

## Anomaly detection
```
Technology:   Rules engine + Isolation Forest (scikit-learn, presumed) + graph/Louvain
              community detection (presumed networkx or igraph)
Purpose:      Three-layer unusual-pattern detection
Why chosen:   More rigorous than a single-method approach; combining
              interpretable rules with statistical outlier detection and
              relational/graph detection is a legitimate defense against any
              single method's blind spots
Exact libraries: PENDING — requires original plan
```

## AI / LLM
```
Primary:      Groq (fast inference, generous-looking free tier that is in
               practice tight — see AI_ML.md)
Fallback:      Gemini — model generation MUST be reconfirmed at build time.
               Gemini 1.5 discontinued; Gemini 2.0 Flash/Flash-Lite shut down
               1 June 2026; Gemini 2.5 generation has an announced retirement
               no earlier than 16 October 2026. Verified current GA as of
               2026-09-21: Gemini 3.1 Flash / Flash-Lite.
Final fallback: Response cache, then static template / 10 golden queries
Why a 4-stage chain: Free-tier LLM rate limits are real and tight enough to
               plausibly exhaust mid-demo (Groq: ~30 req/min, ~1,000 req/day
               per model, varies — see AI_ML.md). This makes the fallback
               chain load-bearing infrastructure, not a nice-to-have.
```

## SQL safety layer
```
Technology:   sqlglot (SQL parsing/allowlisting)
Purpose:      Validate LLM-generated SQL before execution against read-only DuckDB
Why chosen:   Most teams doing NL-to-SQL skip this; per the PS-compliance
              review, this defends directly against a judge trying to break
              the system live with a hostile query
```

## Migration / alternative notes
- If AWS account verification blocks the team (see KNOWN_ISSUES_RISKS.md item C), the plan's own fallback is "host on free non-AWS services" — flagged in the source review as contradicting the PS's explicit AWS deployment requirement. Treat this as a last resort, not a parallel option, and document clearly in the deck if it's invoked.
- Do not assume any currently-free AWS or LLM service remains free indefinitely — re-verify limits at build time per [COST_PLAN.md](./COST_PLAN.md).
