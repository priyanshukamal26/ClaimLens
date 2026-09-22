import { useState, useEffect, useCallback } from 'react'
import { AlertTriangle, Eye, ChevronDown, CheckCircle2 } from 'lucide-react'
import { api } from '../api.js'

function AnomalyScoreBar({ score }) {
  const level = score > 0.6 ? 'high' : score > 0.3 ? 'medium' : 'low'
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <div className="anomaly-bar">
        <div className={`anomaly-bar-fill ${level}`} style={{ width: `${Math.min(score * 100, 100)}%` }} />
      </div>
      <span style={{ fontSize: 12, fontWeight: 600, color: level === 'high' ? 'var(--color-status-risk)' : level === 'medium' ? 'var(--color-status-insight)' : 'var(--color-ink)' }}>
        {(score * 100).toFixed(0)}
      </span>
    </div>
  )
}

function LayerBreakdown({ layers }) {
  if (!layers || typeof layers !== 'object') return null
  return (
    <div style={{ display: 'flex', gap: 12, fontSize: 11, fontWeight: 500 }}>
      {Object.entries(layers).map(([layer, score]) => (
        <div key={layer} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <div style={{
            width: 6, height: 6, borderRadius: '50%',
            background: score > 0.3 ? 'var(--color-status-insight)' : 'var(--color-sage-tint)',
          }} />
          <span style={{ color: 'rgba(16,19,14,0.55)' }}>
            {layer === 'rules' ? 'Rules' : layer === 'isolation_forest' ? 'IForest' : 'Graph'}:
          </span>
          <span>{(score * 100).toFixed(0)}</span>
        </div>
      ))}
    </div>
  )
}

function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000)
    return () => clearTimeout(timer)
  }, [onClose])
  return (
    <div style={{
      position: 'fixed', top: 24, right: 24, zIndex: 100,
      background: type === 'Investigate' ? '#163300' : 'var(--color-sage-ink)',
      color: '#fff', padding: '14px 24px', borderRadius: 12,
      display: 'flex', alignItems: 'center', gap: 10,
      boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
      animation: 'slideIn 0.3s ease-out',
      fontSize: 14, fontWeight: 600,
    }}>
      <CheckCircle2 size={18} style={{ color: '#9FE870' }} />
      {message}
    </div>
  )
}

export default function ReviewQueue() {
  const [queue, setQueue] = useState({ items: [], total: 0 })
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedClaim, setSelectedClaim] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [lobFilter, setLobFilter] = useState('')
  const [toast, setToast] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const [q, s] = await Promise.all([
          api.getAnomalyQueue(lobFilter ? { lob: lobFilter } : {}),
          api.getAnomalyStats(),
        ])
        setQueue(q)
        setStats(s)
      } catch (e) {
        console.error('Failed to load queue:', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [lobFilter])

  async function viewDetail(claimId) {
    setDetailLoading(true)
    try {
      const detail = await api.getAnomalyDetail(claimId)
      setSelectedClaim(detail)
    } catch (e) {
      console.error('Failed to load detail:', e)
    } finally {
      setDetailLoading(false)
    }
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 className="text-heading" style={{ fontSize: 28 }}>Review Queue</h1>
          <p className="text-body-light" style={{ fontSize: 14, marginTop: 4 }}>
            Ranked by anomaly score. Every item is an insight requiring human review.
          </p>
        </div>
        {stats && (
          <div style={{ display: 'flex', gap: 16 }}>
            <div className="kpi-card" style={{ padding: '16px 20px' }}>
              <div className="kpi-value" style={{ fontSize: '1.5rem' }}>{stats.flagged}</div>
              <div className="kpi-label">Flagged</div>
            </div>
            <div className="kpi-card" style={{ padding: '16px 20px' }}>
              <div className="kpi-value" style={{ fontSize: '1.5rem', color: 'var(--color-status-risk)' }}>{stats.high_risk}</div>
              <div className="kpi-label">High Risk</div>
            </div>
          </div>
        )}
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
        <div className="tab-list">
          {['', 'Health', 'Motor', 'Fire', 'Marine', 'Miscellaneous'].map(l => (
            <button key={l} className={`tab ${lobFilter === l ? 'active' : ''}`} onClick={() => setLobFilter(l)}>
              {l || 'All'}
            </button>
          ))}
        </div>
      </div>

      {/* Queue Table */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Claim ID</th>
              <th>Amount</th>
              <th>LOB</th>
              <th>State</th>
              <th>Date</th>
              <th>Status</th>
              <th>Anomaly Score</th>
              <th>Layer Breakdown</th>
              <th>Badge</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              Array.from({ length: 8 }).map((_, i) => (
                <tr key={i}>
                  {Array.from({ length: 10 }).map((_, j) => (
                    <td key={j}><div className="skeleton" style={{ height: 16, width: j === 7 ? 150 : 80 }} /></td>
                  ))}
                </tr>
              ))
            ) : queue.items?.length === 0 ? (
              <tr><td colSpan={10} style={{ textAlign: 'center', padding: 40, color: 'rgba(16,19,14,0.4)' }}>No anomalies matching criteria</td></tr>
            ) : (
              queue.items?.map(item => (
                <tr key={item.claim_id} style={{ cursor: 'pointer' }} onClick={() => viewDetail(item.claim_id)}>
                  <td style={{ fontWeight: 600, fontFamily: 'monospace', fontSize: 13 }}>{item.claim_id}</td>
                  <td>₹{Number(item.claim_amount).toLocaleString('en-IN', { maximumFractionDigits: 0 })}</td>
                  <td>{item.line_of_business}</td>
                  <td>{item.state}</td>
                  <td style={{ fontSize: 13 }}>{item.claim_date}</td>
                  <td>
                    <span className={`badge ${item.status === 'Under Investigation' ? 'badge-risk' : 'badge-insight'}`}>
                      {item.status}
                    </span>
                  </td>
                  <td><AnomalyScoreBar score={item.anomaly_score} /></td>
                  <td><LayerBreakdown layers={item.anomaly_layers} /></td>
                  <td><span className="badge badge-insight"><AlertTriangle size={10} /> INSIGHT</span></td>
                  <td><Eye size={16} style={{ color: 'rgba(16,19,14,0.3)' }} /></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Detail Modal */}
      {selectedClaim && (
        <div
          style={{
            position: 'fixed', inset: 0, background: 'rgba(16,19,14,0.5)', zIndex: 50,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
          onClick={() => setSelectedClaim(null)}
        >
          <div className="card" style={{ maxWidth: 600, width: '90%', maxHeight: '80vh', overflow: 'auto' }} onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 20 }}>
              <div>
                <h3 className="text-heading" style={{ fontSize: 20 }}>Claim Detail</h3>
                <span style={{ fontFamily: 'monospace', fontSize: 14, color: 'rgba(16,19,14,0.5)' }}>{selectedClaim.claim_id}</span>
              </div>
              <span className="badge badge-insight"><AlertTriangle size={10} /> INSIGHT — NOT A DECISION</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px 24px' }}>
              {[
                ['Claim Amount', `₹${Number(selectedClaim.claim_amount).toLocaleString('en-IN')}`],
                ['Anomaly Score', `${(selectedClaim.anomaly_score * 100).toFixed(1)}`],
                ['Policyholder', selectedClaim.policyholder_name],
                ['LOB', selectedClaim.line_of_business],
                ['State', selectedClaim.state],
                ['Insurer', selectedClaim.insurer],
                ['Claim Date', selectedClaim.claim_date],
                ['Status', selectedClaim.status],
                ['Hospital', selectedClaim.hospital_name || '—'],
                ['Garage', selectedClaim.garage_name || '—'],
                ['Agent', selectedClaim.agent_name || '—'],
                ['Agent Region', selectedClaim.agent_region || '—'],
              ].map(([label, val]) => (
                <div key={label}>
                  <div style={{ fontSize: 11, fontWeight: 500, color: 'rgba(16,19,14,0.45)', marginBottom: 2 }}>{label}</div>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>{val}</div>
                </div>
              ))}
            </div>
            {selectedClaim.anomaly_layers && (
              <div style={{ marginTop: 20, padding: '16px', background: 'var(--color-canvas)', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 8, color: 'rgba(16,19,14,0.5)' }}>LAYER BREAKDOWN</div>
                <LayerBreakdown layers={selectedClaim.anomaly_layers} />
              </div>
            )}
            <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
              <button className="btn btn-primary" onClick={async () => {
                await api.createDecision({
                  claim_id: selectedClaim.claim_id,
                  insight_type: 'Anomaly',
                  decision_type: 'Investigate',
                  decided_by: 'Reviewer',
                })
                setToast({ message: `${selectedClaim.claim_id} marked for Investigation`, type: 'Investigate' })
                setSelectedClaim(null)
              }}>
                Investigate
              </button>
              <button className="btn btn-ghost" onClick={async () => {
                await api.createDecision({
                  claim_id: selectedClaim.claim_id,
                  insight_type: 'Anomaly',
                  decision_type: 'Dismiss',
                  decided_by: 'Reviewer',
                })
                setToast({ message: `${selectedClaim.claim_id} dismissed`, type: 'Dismiss' })
                setSelectedClaim(null)
              }}>
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}
