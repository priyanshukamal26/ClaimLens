# ARCHITECTURE.md

## Architecture overview
ClaimLens Nexus is a single-page React app served from S3/CloudFront, talking to a FastAPI backend running on Lambda, backed by DynamoDB for application data and a read-only DuckDB analytics layer for the NL-to-SQL agent. Anomaly detection runs as a batch/pipeline process (rules + Isolation Forest + graph/Louvain) over ingested synthetic data. External context comes from IRDAI/PMFBY panels. LLM calls route through a fallback chain (Groq → Gemini → cache → static template) to survive free-tier rate limits during a live demo.

## Component architecture

```mermaid
flowchart TD
    User[Browser] --> CF[CloudFront + S3<br/>React/Vite/Tailwind SPA]
    CF --> APIGW[API Gateway]
    APIGW --> Lambda[FastAPI on Lambda]
    Lambda --> Dynamo[(DynamoDB<br/>app data, decision log)]
    Lambda --> DuckDB[(Read-only DuckDB<br/>analytics layer)]
    Lambda --> Detect[Anomaly Detection Pipeline<br/>Rules + Isolation Forest + Graph/Louvain]
    Lambda --> Agent[Ask ClaimLens Agent Chain<br/>router→planner→SQL writer→guard→verifier→narrator]
    Agent --> Groq[Groq API]
    Agent -->|fallback| Gemini[Gemini API]
    Agent -->|fallback| Cache[(Response cache)]
    Agent -->|final fallback| Template[Static template / 10 golden queries]
    Lambda --> External[IRDAI / PMFBY / data.gov.in panels]
```

## Data flow — Ask ClaimLens request

```mermaid
sequenceDiagram
    participant U as User
    participant FE as React SPA
    participant API as FastAPI/Lambda
    participant Agent as Agent Chain
    participant DB as Read-only DuckDB
    participant LLM as Groq/Gemini

    U->>FE: Types natural-language question
    FE->>API: POST query
    API->>Agent: route(query)
    Agent->>LLM: plan + write SQL
    LLM-->>Agent: candidate SQL
    Agent->>Agent: guard (sqlglot allowlist check)
    Agent->>DB: execute (read-only)
    DB-->>Agent: result rows
    Agent->>Agent: verify result
    Agent->>LLM: narrate result
    LLM-->>Agent: narrated answer
    Agent-->>API: answer + SQL shown for transparency
    API-->>FE: response
    FE-->>U: shows answer, badged INSIGHT, never DECISION
```

## Anomaly detection flow (three layers)

```mermaid
flowchart LR
    Ingest[Ingested claim] --> Rules[Layer 1: Rules engine]
    Ingest --> IForest[Layer 2: Isolation Forest]
    Ingest --> Graph[Layer 3: Graph / Louvain communities]
    Rules --> Score[Combined anomaly score]
    IForest --> Score
    Graph --> Score
    Score --> Queue[Ranked review queue]
    Queue -->|human review| Decision[Decision Log]
```

## Authentication flow
`PENDING — requires original plan.` No auth mechanism was specified in the source material.

## Deployment flow
See [DEPLOYMENT.md](./DEPLOYMENT.md) for the full AWS build order and the Lambda Function URL permissions gotcha.

## Development vs. production environment
`PENDING — requires original plan` for exact environment-variable and local-dev setup. Known constraint: AWS free-tier ceilings apply to production; local development should not assume unlimited LLM calls given Groq/Gemini rate limits.

## Failure scenarios (known, from verification pass)
- Groq daily/per-minute quota exhausted mid-demo → must fall back to Gemini → cache → static template without visibly breaking
- Gemini model ID stale/retired → agent chain fails outright unless model ID is reconfirmed at build time
- Lambda Function URL returns 403 → missing one of two required IAM permissions
- New AWS account flagged for manual review → account unusable for hours; no AWS-compliant fallback currently documented (see KNOWN_ISSUES_RISKS.md item C)

## Scalability considerations
Not a stated requirement for this hackathon submission; free-tier ceilings are the binding constraint, not scale. See [COST_PLAN.md](./COST_PLAN.md).

## Security boundaries
- DuckDB analytics layer is read-only with external access disabled (hardened execution)
- SQL agent output is filtered through a sqlglot allowlist before execution
- Lambda's own sandbox provides an additional isolation layer
This is a genuine defense-in-depth pattern per DuckDB's own published security guidance, not overkill for an LLM-generated-SQL surface — see [AI_ML.md](./AI_ML.md).
