# ROADMAP.md — Future Work & Phased Expansion

ClaimLens Nexus is currently at MVP state (Phase 1). This roadmap outlines the strategic direction for future iterations.

## Phase 1: The Hackathon MVP (Current)
- [x] Dual-Database Architecture (SQLite + DuckDB)
- [x] Synthetic Data Engine (Policies, Claims, Hospitals, Garages, Agents)
- [x] 3-Layer Anomaly Detection (Rules, Isolation Forest, Graph/Louvain)
- [x] Natural Language to SQL Agent (Ask ClaimLens)
- [x] SQL Guardrail System (`sqlglot` allowlist)
- [x] Executive Overview with Regulatory Context (IRDAI, PMFBY)
- [x] Prioritized Review Queue & Decision Log

## Phase 2: Data Integration & Pipeline Hardening (Next 3 Months)
- **Live Data Ingestion**: Replace the synthetic data engine with Apache Kafka or AWS Kinesis streams for real-time claims ingestion.
- **dbt Integration**: Implement dbt (Data Build Tool) on top of DuckDB for governed, version-controlled SQL transformations before they reach the LLM.
- **Enhanced Entity Resolution**: Improve the graph community detection to handle fuzzy matching (e.g., misspelled hospital names, shared phone numbers).

## Phase 3: Advanced AI Capabilities (6 Months)
- **Multi-Agent Orchestration**: Upgrade `Ask ClaimLens` to a true multi-agent system. Introduce a "Data Analyst Agent" for SQL generation and a "Compliance Agent" that reviews the results against IRDAI regulations before presenting them to the user.
- **Explainable AI (XAI)**: Replace generic SHAP-style explanations with localized, plain-English narrations of *why* the Isolation Forest flagged a specific dimension.
- **Document OCR Pipeline**: Integrate AWS Textract or Google Cloud Vision to extract structured data from uploaded PDF medical bills and cross-reference them against the claim data.

## Phase 4: Production Deployment & Scale (9-12 Months)
- **Cloud Architecture**: Migrate SQLite to Amazon Aurora PostgreSQL (for operational writes) and run DuckDB inside AWS Lambda/Fargate for serverless analytical scaling.
- **Enterprise Auth**: Integrate SSO via Auth0 or Azure AD, including Role-Based Access Control (RBAC) so executives see different dashboards than investigators.
- **Mobile Companion App**: A simplified React Native app for field investigators to log decisions and upload photos directly into the system.
