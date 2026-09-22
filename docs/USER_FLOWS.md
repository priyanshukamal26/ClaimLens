# USER_FLOWS.md — Core User Journeys

ClaimLens Nexus is designed for two primary user personas:
1. **The Executive/Director**: Needs high-level portfolio oversight, regulatory context, and daily briefings.
2. **The Fraud Investigator/Reviewer**: Needs a prioritized queue, deep-dive anomaly explanations, and a fast decision-making workflow.

---

## Flow 1: The Executive Morning Routine

**Goal:** Understand the portfolio's health and regulatory standing at a glance.

1. **Login & Landing**: The executive opens the app and lands on the **Executive Overview** (`/app/overview`).
2. **KPI Check**: They immediately see the hero band: Total Claims, Loss Ratio (e.g., 81%), and Settlement Rate.
3. **Regulatory Context**: They scroll to the Regulatory Panel to compare the internal 81% loss ratio against the live IRDAI industry average (82.88%). They confirm the portfolio is performing within safe boundaries.
4. **Morning Briefing**: They click **Morning Brief** (`/app/brief`) on the sidebar to read the AI-synthesized narrative of the day's top risks, avoiding the need to manually parse raw data.

---

## Flow 2: The Investigator Review Cycle

**Goal:** Process flagged claims efficiently, backed by clear AI rationale.

1. **Queue Access**: The investigator opens the **Review Queue** (`/app/review`).
2. **Triage**: They see a ranked list of claims sorted by anomaly score. They select the highest-scoring claim (e.g., Score: 0.95).
3. **Drill-Down Analysis**: The right-hand pane opens, revealing the 3-Layer Anomaly Breakdown:
   - *Rules*: Flagged because claim amount > policy premium.
   - *Isolation Forest*: Flagged as a statistical outlier for this LOB.
   - *Graph/Louvain*: Flagged because this hospital/garage combination is part of a known high-risk community.
4. **Decision Action**: Armed with clear rationale, the investigator clicks **Investigate**.
5. **Feedback**: A green toast notification confirms the action.
6. **Next Item**: The claim is removed from the queue, and the investigator moves to the next highest-scoring claim.

---

## Flow 3: The Ad-Hoc Data Request (Ask ClaimLens)

**Goal:** Answer a specific business question without writing SQL or waiting for a data team.

1. **Trigger**: An executive asks the investigator: "Which hospitals in Maharashtra have the highest anomaly rates?"
2. **Query Interface**: The investigator opens **Ask ClaimLens** (`/app/ask`).
3. **Natural Language Input**: They type: "Show me the top 5 hospitals in Maharashtra by average anomaly score."
4. **LLM Processing**: The system routes the question to the LLM, generates the SQL, passes it through the `sqlglot` Guard, and executes it against the read-only DuckDB analytics layer.
5. **Result & Narration**: The investigator receives a natural language answer ("The top 5 hospitals are..."), alongside a data table and the exact SQL used to generate the result.
6. **Confidence Check**: The investigator sees the "Source: Groq (llama-3.1)" badge, confirming a live LLM generated the answer safely.

---

## Flow 4: The Audit Trail (Decision Log)

**Goal:** Review past decisions for compliance or QA purposes.

1. **Log Access**: A QA manager opens the **Decision Log** (`/app/decisions`).
2. **Review**: They see a chronological list of all human decisions (Investigate, Dismiss, Escalate, Approve).
3. **Live Sync**: The list is instantly up-to-date, reading directly from the operational SQLite store (unlike the DuckDB analytics layer, which updates asynchronously).
4. **Statistics**: They check the summary stats to see the ratio of Investigations to Dismissals for the week.
