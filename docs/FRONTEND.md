# FRONTEND.md — Frontend Architecture & Design System

The ClaimLens Nexus frontend is a React + Vite Single Page Application (SPA).

## Technology Stack
- **Framework**: React 18, Vite
- **Routing**: `react-router-dom`
- **Charting**: `recharts` (Bar, Line, Pie charts)
- **Icons**: `lucide-react`
- **Styling**: Vanilla CSS (`index.css`) + CSS Variables

## Architecture

The frontend is intentionally kept simple and un-opinionated. It follows a standard component-based architecture:

```
frontend/
├── src/
│   ├── api.js           # Centralized API client (fetch wrappers)
│   ├── App.jsx          # Router & Sidebar Layout
│   ├── index.css        # Design System Tokens & Global Styles
│   ├── main.jsx         # React Entry Point
│   └── pages/           # Route-level components
│       ├── LandingPage.jsx
│       ├── ExecutiveOverview.jsx
│       ├── ReviewQueue.jsx
│       ├── AskClaimLens.jsx
│       ├── DecisionLog.jsx
│       └── MorningBrief.jsx
```

## API Client (`api.js`)

All communication with the FastAPI backend goes through `api.js`. This centralizes error handling and JSON parsing.

- **Base URL**: `/api` (proxied in Vite config during development)
- **Functions**: `getOverview()`, `getAnomalyQueue()`, `askQuestion()`, `createDecision()`, etc.

## Design System

Per `UI_UX_DESIGN_SYSTEM.md`, the UI is inspired by Wise (fintech). We use a custom CSS variable system rather than Tailwind to maintain absolute control over the high-contrast, structural aesthetic.

### Core Colors
- **Brand**: Lime (`#9FE870`)
- **Backgrounds**: Canvas (`#F9F9F8`), Forest (`#163300`)
- **Text**: Primary (`#10130E`), Secondary (`rgba(16,19,14,0.6)`)
- **Alerts**: Sage Ink (`#2A4D14`), Rust (`#A03A2B`)

### Typography
- **Font**: Inter (sans-serif)
- **Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold), 800 (extrabold)

### UI Components
Rather than abstracting every button into a React component, we use CSS classes applied to standard HTML elements:
- `.btn`: Base button styling
- `.btn-primary`: Forest background, white text
- `.btn-ghost`: Transparent background, hover effect
- `.card`: White container with subtle shadow and border radius
- `.text-ui`: Standard structural text styling

## State Management

State is managed locally within route components using standard React Hooks (`useState`, `useEffect`).
- Loading states (`loading`, `detailLoading`) are used to prevent flashing before data arrives.
- Toast notifications (`toast`) provide immediate user feedback after actions (e.g., in `ReviewQueue.jsx`).

## Routing Flow

1. User arrives at `/` (Public Landing Page).
2. User clicks "Enter Application".
3. Redirected to `/app/overview` (Executive Overview).
4. The `AppLayout` component mounts, rendering the Sidebar and the active page inside the `<main>` container.
