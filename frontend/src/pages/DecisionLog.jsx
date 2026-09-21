import { useState, useEffect } from 'react'
import { BookCheck, Clock, Search } from 'lucide-react'
import { api } from '../api.js'

export default function DecisionLog() {
  const [decisions, setDecisions] = useState({ items: [] })
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [d, s] = await Promise.all([
          api.getDecisions(),
          api.getDecisionStats(),
        ])
        setDecisions(d)
        setStats(s)
      } catch (e) {
        console.error('Failed to load decisions:', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const typeColors = {
    Investigate: 'var(--color-status-insight)',
    Escalate: 'var(--color-status-risk)',
    Dismiss: 'rgba(16,19,14,0.4)',
    Approve: 'var(--color-brand-lime)',
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 className="text-heading" style={{ fontSize: 28 }}>Decision Log</h1>
          <p className="text-body-light" style={{ fontSize: 14, marginTop: 4 }}>
            Human decisions made on flagged insights. The system surfaces insights — humans decide.
          </p>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div style={{ display: 'flex', gap: 16, marginBottom: 24 }}>
          {[
            { label: 'Total Decisions', value: stats.total_decisions, color: 'var(--color-ink)' },
            { label: 'Investigate', value: stats.investigate, color: typeColors.Investigate },
            { label: 'Escalate', value: stats.escalate, color: typeColors.Escalate },
            { label: 'Dismiss', value: stats.dismiss, color: typeColors.Dismiss },
            { label: 'Approve', value: stats.approve, color: typeColors.Approve },
          ].map(s => (
            <div key={s.label} className="kpi-card" style={{ padding: '16px 20px', flex: 1 }}>
              <div className="kpi-value" style={{ fontSize: '1.5rem', color: s.color }}>{s.value || 0}</div>
              <div className="kpi-label">{s.label}</div>
            </div>
          ))}
        </div>
      )}

      {/* Decision entries */}
      <div>
        {loading ? (
          Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="log-entry" style={{ marginBottom: 8 }}>
              <div className="skeleton" style={{ height: 20, width: 200, background: 'rgba(255,255,255,0.1)' }} />
              <div className="skeleton" style={{ height: 20, width: 100, background: 'rgba(255,255,255,0.1)' }} />
            </div>
          ))
        ) : decisions.items?.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: 60 }}>
            <BookCheck size={40} style={{ color: 'rgba(16,19,14,0.15)', marginBottom: 16 }} />
            <h3 className="text-ui" style={{ fontSize: 16, marginBottom: 8, color: 'rgba(16,19,14,0.4)' }}>No decisions yet</h3>
            <p className="text-body-light" style={{ fontSize: 14 }}>
              Decisions appear here when a reviewer acts on a flagged insight in the Review Queue.
            </p>
          </div>
        ) : (
          decisions.items?.map((dec, i) => (
            <div key={i} className="log-entry">
              <div style={{ display: 'flex', alignItems: 'center', gap: 16, flex: 1 }}>
                <span className="badge badge-decision">
                  <BookCheck size={10} /> DECISION
                </span>
                <div>
                  <div style={{ fontWeight: 600, fontSize: 14 }}>
                    {dec.decision_type} — {dec.claim_id}
                  </div>
                  <div style={{ fontSize: 12, color: 'rgba(255,255,255,0.5)', marginTop: 2 }}>
                    {dec.line_of_business} · {dec.state} · ₹{Number(dec.claim_amount || 0).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-brand-lime)' }}>
                  {dec.decided_by}
                </div>
                <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.4)', display: 'flex', alignItems: 'center', gap: 4, justifyContent: 'flex-end' }}>
                  <Clock size={10} />
                  {new Date(dec.decided_at).toLocaleString()}
                </div>
              </div>
              {dec.rationale && (
                <div style={{ fontSize: 12, color: 'rgba(255,255,255,0.6)', fontStyle: 'italic', marginTop: 4 }}>
                  {dec.rationale}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
