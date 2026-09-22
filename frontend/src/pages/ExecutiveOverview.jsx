import { useState, useEffect } from 'react'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp, TrendingDown, Minus, AlertTriangle, Shield, Leaf } from 'lucide-react'
import { api } from '../api.js'

const LOB_COLORS = {
  Health: '#9FE870',
  Motor: '#C98A2E',
  Fire: '#B3452F',
  Marine: '#163300',
  Miscellaneous: '#6B8F5B',
}

function KPICard({ label, value, format, trend }) {
  const display = format === 'currency'
    ? `₹${(value / 10000000).toFixed(1)}Cr`
    : format === 'percent'
    ? `${value?.toFixed(1)}%`
    : format === 'number'
    ? Number(value || 0).toLocaleString('en-IN')
    : value

  return (
    <div className="hero-kpi">
      <div className="kpi-value">{display}</div>
      <div className="kpi-label">{label}</div>
    </div>
  )
}

function LobTabs({ active, onChange, lobs }) {
  return (
    <div className="tab-list">
      <button className={`tab ${!active ? 'active' : ''}`} onClick={() => onChange(null)}>All</button>
      {lobs.map(l => (
        <button key={l} className={`tab ${active === l ? 'active' : ''}`} onClick={() => onChange(l)}>
          {l}
        </button>
      ))}
    </div>
  )
}

export default function ExecutiveOverview() {
  const [overview, setOverview] = useState(null)
  const [monthly, setMonthly] = useState([])
  const [byLob, setByLob] = useState([])
  const [byState, setByState] = useState([])
  const [irdai, setIrdai] = useState(null)
  const [pmfby, setPmfby] = useState(null)
  const [activeLob, setActiveLob] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [ov, mon, lob, st, ir, pm] = await Promise.all([
          api.getOverview(),
          api.getMonthlyTrends(activeLob ? { lob: activeLob } : {}),
          api.getTrendsByLOB(),
          api.getTrendsByState(),
          api.getIRDAI().catch(() => null),
          api.getPMFBY().catch(() => null),
        ])
        setOverview(ov)
        setMonthly(mon)
        setByLob(lob)
        setByState(st)
        setIrdai(ir)
        setPmfby(pm)
      } catch (e) {
        console.error('Failed to load overview:', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [activeLob])

  if (loading) {
    return (
      <div>
        <h1 className="text-heading" style={{ fontSize: 28, marginBottom: 24 }}>Executive Overview</h1>
        <div className="hero-band" style={{ marginBottom: 32 }}>
          {[1,2,3,4,5,6].map(i => (
            <div key={i} className="hero-kpi">
              <div className="skeleton" style={{ height: 48, width: 120, marginBottom: 8 }} />
              <div className="skeleton" style={{ height: 16, width: 80 }} />
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 className="text-heading" style={{ fontSize: 28 }}>Executive Overview</h1>
        <span className="badge badge-insight">
          <AlertTriangle size={12} />
          {overview?.anomalies_flagged || 0} insights pending review
        </span>
      </div>

      {/* Hero KPI Band */}
      <div className="hero-band" style={{ marginBottom: 32 }}>
        <KPICard label="Total Policies" value={overview?.total_policies} format="number" />
        <KPICard label="Total Claims" value={overview?.total_claims} format="number" />
        <KPICard label="Gross Premium" value={overview?.total_premium} format="currency" />
        <KPICard label="Loss Ratio" value={overview?.loss_ratio} format="percent" />
        <KPICard label="Settlement Rate" value={overview?.settlement_rate} format="percent" />
        <KPICard label="Anomalies Flagged" value={overview?.anomalies_flagged} format="number" />
      </div>

      {/* LOB Tabs + Monthly Trend Chart */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <h2 className="text-ui" style={{ fontSize: 16 }}>Claims & Loss Ratio Trend</h2>
          <LobTabs active={activeLob} onChange={setActiveLob} lobs={byLob.map(l => l.line_of_business)} />
        </div>
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={monthly}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(16,19,14,0.06)" />
            <XAxis dataKey="month" tick={{ fontSize: 11, fill: 'rgba(16,19,14,0.5)' }} />
            <YAxis yAxisId="left" tick={{ fontSize: 11, fill: 'rgba(16,19,14,0.5)' }} />
            <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11, fill: 'rgba(16,19,14,0.5)' }} />
            <Tooltip
              contentStyle={{
                background: '#163300', color: '#fff', border: 'none',
                borderRadius: 12, fontSize: 13, fontWeight: 500,
              }}
            />
            <Bar yAxisId="left" dataKey="claims_count" fill="#E2F6D5" radius={[4,4,0,0]} name="Claims" />
            <Line yAxisId="right" type="monotone" dataKey="loss_ratio" stroke="#9FE870" strokeWidth={2.5} dot={false} name="Loss Ratio %" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        {/* LOB Breakdown */}
        <div className="card">
          <h2 className="text-ui" style={{ fontSize: 16, marginBottom: 16 }}>By Line of Business</h2>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie
                data={byLob}
                dataKey="claims_count"
                nameKey="line_of_business"
                cx="50%" cy="50%"
                innerRadius={55} outerRadius={90}
                paddingAngle={3}
                strokeWidth={0}
              >
                {byLob.map((entry) => (
                  <Cell key={entry.line_of_business} fill={LOB_COLORS[entry.line_of_business] || '#ccc'} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: '#163300', color: '#fff', border: 'none',
                  borderRadius: 12, fontSize: 13,
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px 16px', marginTop: 8 }}>
            {byLob.map(l => (
              <div key={l.line_of_business} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, fontWeight: 500 }}>
                <div style={{ width: 8, height: 8, borderRadius: '50%', background: LOB_COLORS[l.line_of_business] }} />
                {l.line_of_business}: {l.loss_ratio?.toFixed(1)}%
              </div>
            ))}
          </div>
        </div>

        {/* Top States */}
        <div className="card">
          <h2 className="text-ui" style={{ fontSize: 16, marginBottom: 16 }}>Top States by Claims</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={byState?.slice(0, 8)} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(16,19,14,0.06)" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: 'rgba(16,19,14,0.5)' }} />
              <YAxis dataKey="state" type="category" width={100} tick={{ fontSize: 11, fill: 'rgba(16,19,14,0.7)' }} />
              <Tooltip
                contentStyle={{
                  background: '#163300', color: '#fff', border: 'none',
                  borderRadius: 12, fontSize: 13,
                }}
              />
              <Bar dataKey="claims_count" fill="#9FE870" radius={[0,6,6,0]} name="Claims" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* IRDAI & PMFBY Regulatory Reference Panel (FR-009) */}
      {(irdai || pmfby) && (
        <div style={{ marginTop: 24 }}>
          <h2 className="text-ui" style={{ fontSize: 16, marginBottom: 16 }}>Regulatory Context (Real Data)</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
            {irdai && (
              <div className="card">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
                  <Shield size={20} style={{ color: '#163300' }} />
                  <h3 className="text-ui" style={{ fontSize: 15, margin: 0 }}>IRDAI Regulatory Framework</h3>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px 24px', marginBottom: 16 }}>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 500, color: 'rgba(16,19,14,0.45)', marginBottom: 2 }}>Incurred Claims Ratio FY24-25</div>
                    <div style={{ fontSize: 20, fontWeight: 700 }}>{irdai.incurred_claims_ratio?.fy2024_25}%</div>
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 500, color: 'rgba(16,19,14,0.45)', marginBottom: 2 }}>Claims Settled (Count)</div>
                    <div style={{ fontSize: 20, fontWeight: 700 }}>~{irdai.claims_settled_by_count?.value}%</div>
                  </div>
                </div>
                <div style={{ background: 'var(--color-canvas)', borderRadius: 'var(--radius-sm)', padding: 12 }}>
                  <div style={{ fontSize: 11, fontWeight: 600, color: 'rgba(16,19,14,0.5)', marginBottom: 6 }}>FRAUD FRAMEWORK</div>
                  <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>{irdai.fraud_framework?.name}</div>
                  <div style={{ fontSize: 12, color: 'rgba(16,19,14,0.6)' }}>Status: {irdai.fraud_framework?.status}</div>
                  <ul style={{ margin: '8px 0 0 0', padding: '0 0 0 16px', fontSize: 12, color: 'rgba(16,19,14,0.6)' }}>
                    {irdai.fraud_framework?.key_requirements?.map((req, i) => (
                      <li key={i} style={{ marginBottom: 2 }}>{req}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
            {pmfby && (
              <div className="card">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
                  <Leaf size={20} style={{ color: '#163300' }} />
                  <h3 className="text-ui" style={{ fontSize: 15, margin: 0 }}>PMFBY (Crop Insurance)</h3>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px 24px', marginBottom: 16 }}>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 500, color: 'rgba(16,19,14,0.45)', marginBottom: 2 }}>Total Applications</div>
                    <div style={{ fontSize: 20, fontWeight: 700 }}>{pmfby.national_summary?.total_applications}</div>
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 500, color: 'rgba(16,19,14,0.45)', marginBottom: 2 }}>Total Claims Paid</div>
                    <div style={{ fontSize: 20, fontWeight: 700 }}>{pmfby.national_summary?.total_claims_paid}</div>
                  </div>
                </div>
                <div style={{ background: 'var(--color-canvas)', borderRadius: 'var(--radius-sm)', padding: 12 }}>
                  <div style={{ fontSize: 11, fontWeight: 600, color: 'rgba(16,19,14,0.5)', marginBottom: 6 }}>DATA SOURCE</div>
                  <div style={{ fontSize: 12, color: 'rgba(16,19,14,0.6)' }}>{pmfby.state_claims_paid?.source}</div>
                  <div style={{ fontSize: 11, color: 'rgba(16,19,14,0.45)', marginTop: 4 }}>License: {pmfby.state_claims_paid?.license}</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
