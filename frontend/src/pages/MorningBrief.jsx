import { useState, useEffect } from 'react'
import { Sun, TrendingUp, TrendingDown, Minus, AlertTriangle } from 'lucide-react'
import { api } from '../api.js'

export default function MorningBrief() {
  const [brief, setBrief] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const b = await api.getMorningBrief()
        setBrief(b)
      } catch (e) {
        console.error('Failed to load morning brief:', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const TrendIcon = brief?.trend_direction === 'worsening' ? TrendingUp
    : brief?.trend_direction === 'improving' ? TrendingDown
    : Minus

  const trendColor = brief?.trend_direction === 'worsening' ? 'var(--color-status-risk)'
    : brief?.trend_direction === 'improving' ? 'var(--color-brand-lime)'
    : 'rgba(16,19,14,0.4)'

  if (loading) {
    return (
      <div>
        <h1 className="text-heading" style={{ fontSize: 28, marginBottom: 24 }}>Morning Brief</h1>
        <div className="card" style={{ padding: 40 }}>
          <div className="skeleton" style={{ height: 24, width: 300, marginBottom: 16 }} />
          <div className="skeleton" style={{ height: 16, width: '100%', marginBottom: 8 }} />
          <div className="skeleton" style={{ height: 16, width: '80%' }} />
        </div>
      </div>
    )
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
        <div style={{
          width: 40, height: 40, borderRadius: '50%',
          background: 'var(--color-sage-tint)', display: 'flex',
          alignItems: 'center', justifyContent: 'center',
        }}>
          <Sun size={20} style={{ color: 'var(--color-forest)' }} />
        </div>
        <div>
          <h1 className="text-heading" style={{ fontSize: 28 }}>Morning Brief</h1>
          <p className="text-body-light" style={{ fontSize: 13 }}>{brief?.date}</p>
        </div>
      </div>

      {/* Summary Card */}
      <div className="card" style={{ marginBottom: 24, padding: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
          <TrendIcon size={20} style={{ color: trendColor }} />
          <span className="text-ui" style={{
            fontSize: 14, color: trendColor,
            textTransform: 'capitalize',
          }}>
            {brief?.trend_direction} trend
          </span>
        </div>
        <p className="text-body" style={{ fontSize: 16, lineHeight: 1.7 }}>
          {brief?.summary}
        </p>
      </div>

      {/* KPI Snapshot */}
      {brief?.kpi_snapshot && (
        <div className="hero-band" style={{ marginBottom: 24 }}>
          <div className="hero-kpi">
            <div className="kpi-value">{Number(brief.kpi_snapshot.total_policies || 0).toLocaleString('en-IN')}</div>
            <div className="kpi-label">Policies Monitored</div>
          </div>
          <div className="hero-kpi">
            <div className="kpi-value">{Number(brief.kpi_snapshot.total_claims || 0).toLocaleString('en-IN')}</div>
            <div className="kpi-label">Claims Processed</div>
          </div>
          <div className="hero-kpi">
            <div className="kpi-value">{brief.kpi_snapshot.loss_ratio?.toFixed(1)}%</div>
            <div className="kpi-label">Loss Ratio</div>
          </div>
          <div className="hero-kpi">
            <div className="kpi-value">{brief.kpi_snapshot.settlement_rate?.toFixed(1)}%</div>
            <div className="kpi-label">Settlement Rate</div>
          </div>
          <div className="hero-kpi">
            <div className="kpi-value" style={{ color: 'var(--color-status-insight)' }}>
              {brief.kpi_snapshot.anomalies_flagged || 0}
            </div>
            <div className="kpi-label">Insights Pending</div>
          </div>
        </div>
      )}

      {/* Top Anomalies */}
      <div className="card">
        <h2 className="text-ui" style={{ fontSize: 16, marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
          <AlertTriangle size={16} style={{ color: 'var(--color-status-insight)' }} />
          Top Flagged Insights
        </h2>
        {brief?.top_anomalies?.length === 0 ? (
          <p className="text-body-light">No significant anomalies to report today.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {brief?.top_anomalies?.map((anomaly, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                padding: '14px 16px', background: 'var(--color-canvas)',
                borderRadius: 'var(--radius-sm)',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                  <div style={{
                    width: 28, height: 28, borderRadius: '50%',
                    background: anomaly.anomaly_score > 0.6 ? 'var(--color-risk-bg)' : 'var(--color-insight-bg)',
                    color: anomaly.anomaly_score > 0.6 ? 'var(--color-status-risk)' : 'var(--color-status-insight)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontWeight: 800, fontSize: 11,
                  }}>
                    {i + 1}
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 14 }}>
                      {anomaly.claim_id} · ₹{Number(anomaly.claim_amount).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                    </div>
                    <div style={{ fontSize: 12, color: 'rgba(16,19,14,0.5)' }}>
                      {anomaly.line_of_business} · {anomaly.state} · {anomaly.claim_date}
                    </div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span className="badge badge-insight">
                    <AlertTriangle size={10} /> INSIGHT
                  </span>
                  <span style={{
                    fontWeight: 800, fontSize: 16,
                    color: anomaly.anomaly_score > 0.6 ? 'var(--color-status-risk)' : 'var(--color-status-insight)',
                  }}>
                    {(anomaly.anomaly_score * 100).toFixed(0)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
