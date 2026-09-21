# COST_PLAN.md

No service listed here should be treated as permanently free. Ceilings below reflect the independent verification pass (verified 2026-09-21) or are marked for re-verification.

| Service | Purpose | Plan | Verified limit | Risk | Alternative |
|---|---|---|---|---|---|
| AWS Lambda | Backend compute | Free tier | 250 MB unzipped / 50 MB zipped / 6 MB sync response / 15 min max timeout / 1,769 MB = 1 vCPU — CONFIRMED current | Low, if package stays within limits | N/A |
| AWS S3 + CloudFront | Frontend hosting/CDN | Free tier | Not independently re-verified this pass | Medium — verify at build time | N/A |
| DynamoDB | App data | Free tier | Not independently re-verified this pass | Medium — verify at build time | N/A |
| Groq API | Primary LLM | Free tier | ~30 req/min, ~1,000 req/day per model (varies — e.g. `llama-3.1-8b-instant` 14,400/day); token-per-minute caps can bind first — CONFIRMED tight | **High** — plausibly exhausted by rehearsal + live demo | Gemini fallback → cache → static template |
| Gemini API | Fallback LLM | Free tier | Model lifecycle moving fast — see AI_ML.md. Confirm exact current limits alongside model ID at build time | Medium-High — both quota and model-retirement risk | Cache → static template |
| Kaggle datasets | Source data | Free (download) | Licenses: MIT confirmed (mmumairkhattak); CC BY-NC-SA 4.0 confirmed (pyatakov); **unclear/unverified** for balajiadithya and arpan129 | Medium — license-lock before packaging | N/A, must resolve before submission |
| data.gov.in / PIB | Source data | Government Open Data License / public domain | Confirmed | Low | N/A |

## Cost-minimization notes
- The architecture already minimizes paid dependencies by design (free-tier AWS services, free-tier LLM APIs with fallback chain).
- The single largest realistic cost risk is not a metered bill — it's **quota exhaustion breaking the demo**, which is a reliability risk mitigated by the fallback chain, not a cost risk mitigated by a budget.
- New AWS account free-credit eligibility is time-sensitive to account verification status — see DEPLOYMENT.md.

## PENDING — cannot be documented without the original plan
Exact DynamoDB/S3/CloudFront free-tier usage projections against expected demo traffic volume.
