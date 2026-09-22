# PRESENTATION_DECK.md — Slide Content for Hackathon Submission

*Instructions: Copy and paste the text below into your PowerPoint or Google Slides presentation. Use screenshots from the running application for the visual elements.*

---

## Slide 1: Title Slide
**Visual**: Large title, minimal background. Screenshot of the Executive Overview hero band in the bottom corner.
**Title**: ClaimLens Nexus
**Subtitle**: Intelligence without the Black Box.
**Footer**: Innovation Hackathon 2026 | Team BR-[Your Team Number]

---

## Slide 2: The Problem (Track 2)
**Visual**: Icons representing Data Silos, Slow Investigations, and Opaque AI.
**Title**: The "Insurance Insight Nexus" Challenge
**Bullets**:
- **Data Overload**: Insurers are drowning in claims data but struggling to surface actionable insights.
- **The Black Box Problem**: Existing AI systems make automated decisions without explaining *why*, breaking trust and compliance.
- **The Technical Barrier**: Non-technical executives cannot ask ad-hoc questions without a data engineering team.

---

## Slide 3: Our Solution
**Visual**: Screenshot of the "Ask ClaimLens" NL-to-SQL interface.
**Title**: Meet ClaimLens Nexus
**Bullets**:
- **Cloud-Native Intelligence**: A React + FastAPI platform deployed securely on AWS.
- **3-Layer Anomaly Detection**: Rules + Isolation Forest + Graph Community detection working in ensemble.
- **Insight ≠ Decision**: AI flags anomalies; Humans make decisions. Strict separation of operational and analytical data.
- **Agentic AI**: A Natural-Language-to-SQL engine protected by a robust AST parsing guardrail.

---

## Slide 4: Business Value (Judging Criteria: 25%)
**Visual**: Screenshot of the IRDAI/PMFBY Regulatory panel.
**Title**: Measurable Business Impact
**Bullets**:
- **Faster Triage**: Ranked review queues and AI-synthesized Morning Briefs reduce time-to-investigation.
- **Regulatory Grounding**: Real-time integration of public IRDAI and PMFBY data provides a baseline against the synthetic portfolio.
- **Cost Reduction**: Replaces expensive proprietary dashboards with an open-source, LLM-driven query engine.

---

## Slide 5: Technical Excellence & Security (Judging Criteria: 20%)
**Visual**: The Architecture Diagram from `docs/ARCHITECTURE.md`.
**Title**: Defense-in-Depth Architecture
**Bullets**:
- **Dual-Database Design**: SQLite for zero-latency operational writes (Decision Log) and read-only DuckDB for analytical speed.
- **SQL Injection Prevention**: LLM-generated SQL is parsed by `sqlglot` into an AST and checked against a strict allowlist. It is physically impossible for the LLM to DROP tables or exfiltrate data.
- **4-Stage LLM Fallback**: Primary (Groq) → Secondary (Gemini) → Semantic Cache → Golden Templates. The system stays up even if the LLM provider goes down.

---

## Slide 6: UI/UX Innovation (Judging Criteria: 15%)
**Visual**: Split-screen showing the Review Queue Drill-Down pane.
**Title**: Intuitive, Frictionless Workflows
**Bullets**:
- **No Modal Fatigue**: Split-pane drill-downs allow investigators to process claims rapidly.
- **Information Density**: Wise-inspired design language prioritizes contrast and legibility over flashy animations.
- **Instant Feedback**: Toast notifications and a live-syncing Decision Log provide immediate operational confidence.

---

## Slide 7: Next Steps & Roadmap
**Visual**: Timeline graphic.
**Title**: Beyond the Hackathon
**Bullets**:
- **Phase 2**: Real-time Kafka ingestion and dbt integration for governed data transformations.
- **Phase 3**: Explainable AI (XAI) narrations and OCR integration for medical bills.
- **Phase 4**: Enterprise SSO, Role-Based Access Control, and a mobile companion app for field investigators.

---

## Slide 8: Thank You
**Visual**: Team photo or stylized logo.
**Title**: Thank You
**Bullets**:
- **Team**: BR-[Your Team Number]
- **Deliverables**: Code, Architecture, CI/CD, Video, Deck, and Deployment Guide submitted.
- *Any questions?*
