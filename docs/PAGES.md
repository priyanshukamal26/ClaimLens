# PAGES.md — Frontend Inventory

The frontend is a React + Vite Single Page Application (SPA) utilizing `react-router-dom` for navigation.

## Design System
- **Framework**: Custom implementation heavily inspired by Wise (minimalist, high-contrast, data-dense)
- **CSS**: Vanilla CSS with CSS variables (`index.css`)
- **Icons**: `lucide-react`
- **Charts**: `recharts`

## Routes

### `/` (Public Landing Page)
- **Component**: `LandingPage.jsx`
- **Purpose**: Marketing/public entry point explaining the product value proposition.
- **Key Features**: Hero section, value props, architectural diagram visual, animated CTAs to enter the app.

### `/app/*` (Authenticated App Shell)
- **Component**: `AppLayout` (in `App.jsx`)
- **Purpose**: Wraps all dashboard views with the main sidebar navigation.
- **Key Features**: Persistent sidebar, brand logo, navigation links.

## Dashboard Views (Inside `/app`)

### 1. Executive Overview (`/app/overview`)
- **Component**: `ExecutiveOverview.jsx`
- **Purpose**: High-level KPI monitoring for C-suite and directors.
- **Key Features**:
  - Hero KPI band (Total Claims, Loss Ratio, Settlement Rate)
  - 30-Day Trends (Line chart)
  - Risk Distribution (Donut chart)
  - State/LOB breakdowns (Bar charts)
  - **Regulatory Context Panel**: Live data from IRDAI (Incurred Claims Ratio) and PMFBY (Crop Insurance).

### 2. Review Queue (`/app/review`)
- **Component**: `ReviewQueue.jsx`
- **Purpose**: The core workflow for human reviewers/investigators to process AI-flagged claims.
- **Key Features**:
  - Ranked list of claims (highest anomaly score first).
  - LOB filtering.
  - Drill-down pane: When a claim is selected, shows the 3-layer anomaly breakdown.
  - Action buttons: Investigate, Dismiss (writes to SQLite Decision Log).
  - Toast notifications for action feedback.

### 3. Ask ClaimLens (`/app/ask`)
- **Component**: `AskClaimLens.jsx`
- **Purpose**: Natural Language to SQL interface for ad-hoc querying.
- **Key Features**:
  - Chat interface.
  - 4-stage LLM fallback pipeline indicator (Groq → Gemini → Cache → Template).
  - Golden Queries: Pre-populated suggested questions.
  - Transparent SQL execution: Shows the exact generated SQL that the Guard verified.

### 4. Decision Log (`/app/decisions`)
- **Component**: `DecisionLog.jsx`
- **Purpose**: Audit trail of all human decisions made on insights.
- **Key Features**:
  - Chronological list of decisions (Investigate, Escalate, Dismiss, Approve).
  - Live-sync: Reads directly from SQLite for zero-latency updates.
  - Summary statistics cards.

### 5. Morning Brief (`/app/brief`)
- **Component**: `MorningBrief.jsx`
- **Purpose**: Synthesized daily summary of the portfolio's health.
- **Key Features**:
  - AI-generated summary text (simulated/cached).
  - Top 3 highest-risk anomalies requiring immediate attention.
  - Portfolio alerts (e.g., specific hospitals with sudden volume spikes).
