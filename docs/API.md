# API.md — ClaimLens Nexus API Reference

All endpoints are served by the FastAPI backend at `/api/*`. See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full system diagram.

## Health

### `GET /api/health`
| Field | Value |
|-------|-------|
| Purpose | Health check / readiness probe |
| Auth | None |
| Response | `{ "status": "ok" }` |
| Status | IMPLEMENTED |

---

## Trends (FR-002)

### `GET /api/trends/overview`
| Field | Value |
|-------|-------|
| Purpose | KPI summary for Executive Overview hero band |
| Auth | None |
| Response | `{ total_policies, total_claims, total_premium, loss_ratio, settlement_rate, flagged_claims, high_risk_claims }` |
| DB | DuckDB analytics layer (read-only) |
| Status | IMPLEMENTED |

### `GET /api/trends/monthly`
| Field | Value |
|-------|-------|
| Purpose | Monthly claims/premium/loss ratio time series |
| Auth | None |
| Query params | `lob` (optional) — filter by line of business |
| Response | Array of `{ month, total_claims, total_amount, avg_amount, loss_ratio }` |
| DB | DuckDB analytics layer |
| Status | IMPLEMENTED |

### `GET /api/trends/by-lob`
| Field | Value |
|-------|-------|
| Purpose | Aggregates grouped by line of business |
| Auth | None |
| Response | Array of `{ line_of_business, policy_count, claim_count, total_premium, total_claims_amount, loss_ratio }` |
| DB | DuckDB analytics layer |
| Status | IMPLEMENTED |

### `GET /api/trends/by-state`
| Field | Value |
|-------|-------|
| Purpose | Aggregates grouped by state |
| Auth | None |
| Response | Array of `{ state, policy_count, claim_count, total_premium, total_claims_amount, loss_ratio }` |
| DB | DuckDB analytics layer |
| Status | IMPLEMENTED |

---

## Anomalies (FR-003)

### `GET /api/anomalies/queue`
| Field | Value |
|-------|-------|
| Purpose | Ranked review queue of flagged claims (INSIGHT-badged) |
| Auth | None |
| Query params | `min_score` (default 0.2), `lob` (optional), `limit` (default 50), `offset` (default 0) |
| Response | `{ items: [...], total: N }` — each item includes anomaly_score, anomaly_layers JSON, claim details |
| DB | DuckDB analytics layer |
| ADR | ADR-004: every item is an INSIGHT, never a DECISION |
| Status | IMPLEMENTED |

### `GET /api/anomalies/stats`
| Field | Value |
|-------|-------|
| Purpose | Summary statistics (total flagged, high risk, LOB distribution, layer breakdown) |
| Auth | None |
| Response | `{ total_flagged, high_risk, by_lob: [...], by_layer: {...} }` |
| DB | DuckDB analytics layer |
| Status | IMPLEMENTED |

### `GET /api/anomalies/{claim_id}`
| Field | Value |
|-------|-------|
| Purpose | Detailed anomaly breakdown for a single claim |
| Auth | None |
| Response | Claim details + per-layer scores and reasons |
| DB | DuckDB analytics layer |
| Status | IMPLEMENTED |

---

## Ask ClaimLens (FR-004)

### `POST /api/ask`
| Field | Value |
|-------|-------|
| Purpose | Natural-language question → guarded SQL → narrated answer |
| Auth | None |
| Request body | `{ "question": "string" }` |
| Response | `{ answer, sql_used, source, confidence }` — source indicates whether live LLM, golden query, cache, or template |
| Pipeline | Router → Planner → SQL Writer → Guard (sqlglot) → Executor → Verifier → Narrator |
| Fallback chain | Groq → Gemini → Cache → Golden Queries/Template |
| DB | DuckDB analytics layer (read-only, external access disabled) |
| Security | sqlglot allowlist validation before execution (SEC-001) |
| Status | IMPLEMENTED |

---

## Decisions (FR-006)

### `GET /api/decisions/`
| Field | Value |
|-------|-------|
| Purpose | List all decisions in the Decision Log |
| Auth | None |
| Query params | `limit` (default 50), `offset` (default 0) |
| Response | `{ items: [...] }` — each item includes decision details + joined claim/policy info |
| DB | SQLite (live-sync — reads directly from operational store) |
| ADR | ADR-004: this is where INSIGHTs become DECISIONs via human action |
| Status | IMPLEMENTED |

### `POST /api/decisions/`
| Field | Value |
|-------|-------|
| Purpose | Record a human decision on a flagged insight |
| Auth | None |
| Request body | `{ claim_id, insight_type, decision_type, decided_by, rationale? }` |
| Validation | `insight_type` ∈ {Anomaly, Pattern, Ring}; `decision_type` ∈ {Investigate, Escalate, Dismiss, Approve} |
| Response | `{ decision_id, decided_at, message }` |
| DB | SQLite (write) |
| Status | IMPLEMENTED |

### `GET /api/decisions/stats`
| Field | Value |
|-------|-------|
| Purpose | Summary counts by decision type |
| Auth | None |
| Response | `{ total_decisions, investigate, escalate, dismiss, approve }` |
| DB | SQLite (live-sync) |
| Status | IMPLEMENTED |

---

## Morning Brief (FR-005)

### `GET /api/brief/morning`
| Field | Value |
|-------|-------|
| Purpose | Synthesized daily summary of key metrics and top anomalies |
| Auth | None |
| Response | `{ date, overview: {...}, top_anomalies: [...], trends: {...}, action_items: [...] }` |
| DB | DuckDB analytics layer |
| Status | IMPLEMENTED |

---

## External Data (FR-009)

### `GET /api/external/irdai`
| Field | Value |
|-------|-------|
| Purpose | IRDAI regulatory data panel (real verified data, not synthetic) |
| Auth | None |
| Response | `{ source, verified_date, incurred_claims_ratio, claims_settled_by_count, tpa_settlement_share, fraud_framework }` |
| Data | Static verified data from IRDAI Annual Report 2024-25 — see [DATA.md](./DATA.md) |
| Status | IMPLEMENTED |

### `GET /api/external/pmfby`
| Field | Value |
|-------|-------|
| Purpose | PMFBY crop insurance data panel (real verified data) |
| Auth | None |
| Response | `{ national_summary, state_claims_paid }` |
| Data | Static verified data from data.gov.in / PIB — see [DATA.md](./DATA.md) |
| Status | IMPLEMENTED |

---

## Error Responses

All endpoints return standard HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request / validation error |
| 404 | Resource not found |
| 422 | Unprocessable entity (Pydantic validation failure) |
| 500 | Internal server error |

Error response body: `{ "detail": "Human-readable error message" }`

---

## Cross-References
- Security: [AUTH_SECURITY.md](./AUTH_SECURITY.md)
- Database: [DATABASE.md](./DATABASE.md)
- Architecture: [ARCHITECTURE.md](./ARCHITECTURE.md)
- Frontend integration: [FRONTEND.md](./FRONTEND.md)
