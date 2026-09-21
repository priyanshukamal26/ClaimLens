# KNOWN_ISSUES_RISKS.md

Consolidated from both source analyses. Each item has an ID for reference elsewhere in the docs.

| ID | Issue | Severity | Status | Detail |
|---|---|---|---|---|
| A | Time budget | HIGH | OPEN | Source schedule assumes ~22 hours of focused build time; submission is same-day per source material's own timeline. Mitigation: Cut Level 1 as active target (ADR-005), not a reactive fallback. |
| B | Single point of failure — one engineer owns generator, detection, API, frontend integration, and AWS | HIGH | OPEN | 4 of 5 team roles are non-technical (docs, deck, QA) per source material. The "3-5 person team" requirement is satisfied on paper but not in engineering throughput. No documented mitigation beyond scope reduction (Cut Levels). |
| C | AWS account/free-tier risk | HIGH | OPEN | New account verification can take hours if flagged for manual review. Fallback ("free non-AWS hosting") contradicts the PS's AWS requirement. Mitigation: start account creation in Hour 0 (PROJECT_TRACK.md H0.2), no other mitigation currently documented. |
| D | Dataset licensing deferred | MEDIUM | OPEN | balajiadithya and arpan129 Kaggle datasets have unclear/unstated licenses. Must be locked before packaging, not left as a final-hours checklist item. See DATA.md and PROJECT_TRACK.md H0.5. |
| E | LLM dependency / rate-limit risk | MEDIUM-HIGH | OPEN | Groq free tier (~30 req/min, ~1,000 req/day per model) can plausibly be exhausted by rehearsal + live demo. Fallback chain (ADR-003) exists on paper but must be tested end-to-end before the demo — an untested fallback is not a real mitigation. |
| F | Scope vs. differentiation trade-off | MEDIUM | OPEN | The most differentiating features (three-layer detection, held-out pattern eval) are also the most complex and most likely to be cut under time pressure — meaning a panicked cut could remove exactly what earns the Innovation/Business Value score. Mitigation: ADR-004/ADR-001 flagged as protect-from-cuts; decide Cut Level explicitly and once (ADR-005), not reactively. |
| G | Unconfirmed dataset table (TPA hospital counts) | MEDIUM | OPEN | Claimed in the balajiadithya Kaggle file but not confirmed present from the public description. Do not build ingestion code against it until opened and confirmed. See PROJECT_TRACK.md H0.4. |
| H | PMFBY state/district name desync | MEDIUM | OPEN | Dataset author's own notes confirm state/district name strings are not synchronized between the two PMFBY district files, and some states are missing entirely. Budget a real hour, not a quick join. See PROJECT_TRACK.md H0.6. |
| I | Gemini model lifecycle churn | MEDIUM | OPEN | Fast-moving generation retirements (see AI_ML.md). Any hardcoded model ID is a build-time risk. Mitigation: reconfirm in-console every session, not from any document. |
| J | Lambda Function URL 403 | MEDIUM (high if hit late) | OPEN until fixed | Requires both `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction` IAM permissions (Oct 2025 change). Fix on first deploy. See DEPLOYMENT.md. |

## Recommendation (from PS-compliance review, carried forward)
Front-load items A/C/D above in Hour 0 — they are pass/fail blockers that do not scale down gracefully, unlike frontend polish or dashboard breadth, which do.
