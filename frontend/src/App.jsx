import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom'
import { LayoutDashboard, ShieldAlert, MessageSquareText, BookCheck, Sun } from 'lucide-react'
import ExecutiveOverview from './pages/ExecutiveOverview.jsx'
import ReviewQueue from './pages/ReviewQueue.jsx'
import AskClaimLens from './pages/AskClaimLens.jsx'
import DecisionLog from './pages/DecisionLog.jsx'
import MorningBrief from './pages/MorningBrief.jsx'

const NAV_ITEMS = [
  { path: '/overview', label: 'Executive Overview', icon: LayoutDashboard },
  { path: '/review', label: 'Review Queue', icon: ShieldAlert },
  { path: '/ask', label: 'Ask ClaimLens', icon: MessageSquareText },
  { path: '/decisions', label: 'Decision Log', icon: BookCheck },
  { path: '/brief', label: 'Morning Brief', icon: Sun },
]

function Sidebar() {
  return (
    <nav className="sidebar">
      <div style={{ padding: '0 24px', marginBottom: 40 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 32, height: 32, borderRadius: '50%',
            background: 'var(--color-brand-lime)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontWeight: 900, fontSize: 14, color: 'var(--color-forest)',
          }}>CL</div>
          <div>
            <div style={{ fontWeight: 800, fontSize: 16, color: 'white' }}>ClaimLens</div>
            <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.45)', fontWeight: 500 }}>Nexus</div>
          </div>
        </div>
      </div>
      {NAV_ITEMS.map(({ path, label, icon: Icon }) => (
        <NavLink
          key={path}
          to={path}
          className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
        >
          <Icon size={18} />
          {label}
        </NavLink>
      ))}
      <div style={{ marginTop: 'auto', padding: '24px', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
        <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.35)', fontWeight: 400, lineHeight: 1.6 }}>
          Insights, never decisions.<br />
          Every flag requires human review.
        </div>
      </div>
    </nav>
  )
}

function AppLayout() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', width: '100%' }}>
      <Sidebar />
      <main style={{ flex: 1, padding: '32px 40px', overflowY: 'auto', maxHeight: '100vh' }}>
        <Routes>
          <Route path="/" element={<Navigate to="overview" replace />} />
          <Route path="overview" element={<ExecutiveOverview />} />
          <Route path="review" element={<ReviewQueue />} />
          <Route path="ask" element={<AskClaimLens />} />
          <Route path="decisions" element={<DecisionLog />} />
          <Route path="brief" element={<MorningBrief />} />
        </Routes>
      </main>
    </div>
  );
}

import LandingPage from './pages/LandingPage.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        
        {/* Authenticated Dashboard Routes */}
        <Route path="/app/*" element={<AppLayout />} />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
