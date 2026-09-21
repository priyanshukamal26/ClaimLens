# DEPLOYMENT.md

## Target architecture
```
Browser
  ↓
CloudFront + S3        (React/Vite/Tailwind SPA)
  ↓
API Gateway + Lambda    (FastAPI backend)
  ↓
DynamoDB                (app data, decision log)
  ↓
DuckDB (read-only, in-Lambda or attached) + external LLM APIs (Groq/Gemini)
```

## Critical gotcha — Lambda Function URL 403 (confirmed real and currently active)
Since an AWS change in **October 2025**, a Lambda Function URL returns 403 **unless both** of the following IAM permissions are granted:
- `lambda:InvokeFunctionUrl`
- `lambda:InvokeFunction`

This is confirmed as a genuinely common, currently-reported failure mode — multiple live reports of teams hitting this in recent months. **Grant both permissions on the very first deploy.** Do not wait to discover the 403 during integration testing; budget explicit time for this in Hour 0 (see PROJECT_TRACK.md H0.3). This is assessed as one of the single highest-value warnings in the entire source material.

## AWS account requirement
A **brand-new AWS account** is needed to access free credits per the original plan. New account verification can itself take hours if flagged for manual review — this is a plausible, real failure point. **No fully AWS-compliant fallback is currently documented.** The plan's stated fallback ("host on free non-AWS services") contradicts the PS's explicit "AWS Cloud Deployment" requirement — treat this as a last resort only, and if invoked, say so explicitly in the deck rather than glossing over it.

## Lambda limits (confirmed current, 2026-09-21)
```
Unzipped package size:   250 MB
Zipped package size:     50 MB
Sync response limit:     6 MB
Max timeout:              15 minutes
Memory → vCPU:            1,769 MB = 1 vCPU
```

## Build order
```
1. AWS account creation + verification         ← start THIS FIRST, hours-long risk
2. IAM setup (incl. both Lambda invoke perms)   ← second highest priority
3. DynamoDB provisioning
4. Lambda + API Gateway (FastAPI backend)
5. S3 + CloudFront (frontend hosting)
6. Frontend build + deploy
7. CI/CD wiring
8. End-to-end smoke test against deployed URL (not localhost)
```
Exact per-service configuration steps: `PENDING — requires original plan`.

## Free-tier limitations
See [COST_PLAN.md](./COST_PLAN.md) for the full per-service table.

## Production verification checklist (before demo)
- [ ] Deployed URL loads the frontend (not localhost)
- [ ] Ask ClaimLens live query succeeds against deployed backend
- [ ] Fallback chain (Gemini → cache → template) manually triggered and verified to degrade gracefully
- [ ] Lambda Function URL does not 403
- [ ] All 10 golden queries return correct answers via the deterministic path

## PENDING — cannot be documented without the original plan
CI/CD pipeline specifics, exact environment variable list, rollback procedure, domain/HTTPS setup if any beyond default CloudFront.
