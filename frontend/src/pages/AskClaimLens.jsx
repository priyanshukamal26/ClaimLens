import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Sparkles, Code, AlertTriangle } from 'lucide-react'
import { api } from '../api.js'

const SUGGESTED_QUESTIONS = [
  'What is the overall loss ratio?',
  'How many claims have been flagged as anomalies?',
  'Which line of business has the highest loss ratio?',
  'What are the top 5 states by claim volume?',
  'What is the settlement rate?',
  'Which agents have the most claims?',
]

export default function AskClaimLens() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSubmit(question) {
    const q = question || input.trim()
    if (!q) return

    const userMsg = { role: 'user', content: q }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const result = await api.askQuestion(q)
      const botMsg = {
        role: 'assistant',
        content: result.answer,
        sql: result.sql_used,
        source: result.source,
        isInsight: result.is_insight,
      }
      setMessages(prev => [...prev, botMsg])
    } catch (e) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your question. Please try again.',
        source: 'error',
        isInsight: true,
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 64px)' }}>
      <div style={{ marginBottom: 24 }}>
        <h1 className="text-heading" style={{ fontSize: 28 }}>Ask ClaimLens</h1>
        <p className="text-body-light" style={{ fontSize: 14, marginTop: 4 }}>
          Ask questions about the insurance data in plain English. Answers are insights, never decisions.
        </p>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', paddingBottom: 20 }}>
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', padding: '60px 20px' }}>
            <div style={{
              width: 64, height: 64, borderRadius: '50%', margin: '0 auto 20px',
              background: 'var(--color-sage-tint)', display: 'flex', alignItems: 'center',
              justifyContent: 'center',
            }}>
              <Sparkles size={28} style={{ color: 'var(--color-forest)' }} />
            </div>
            <h2 className="text-ui" style={{ fontSize: 18, marginBottom: 8 }}>What would you like to know?</h2>
            <p className="text-body-light" style={{ fontSize: 14, maxWidth: 400, margin: '0 auto 32px' }}>
              Ask about claims trends, anomaly patterns, settlement rates, or any aspect of the insurance portfolio.
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center', maxWidth: 600, margin: '0 auto' }}>
              {SUGGESTED_QUESTIONS.map(q => (
                <button key={q} className="btn btn-ghost" style={{ fontSize: 13 }} onClick={() => handleSubmit(q)}>
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} style={{
            display: 'flex', gap: 12, marginBottom: 20,
            flexDirection: msg.role === 'user' ? 'row-reverse' : 'row',
          }}>
            <div style={{
              width: 32, height: 32, borderRadius: '50%', flexShrink: 0,
              background: msg.role === 'user' ? 'var(--color-forest)' : 'var(--color-sage-tint)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              {msg.role === 'user'
                ? <User size={16} style={{ color: 'white' }} />
                : <Bot size={16} style={{ color: 'var(--color-forest)' }} />
              }
            </div>
            <div style={{
              maxWidth: '70%',
              background: msg.role === 'user' ? 'var(--color-forest)' : 'var(--color-surface)',
              color: msg.role === 'user' ? 'white' : 'var(--color-ink)',
              padding: '14px 18px', borderRadius: 'var(--radius-card)',
              boxShadow: msg.role === 'user' ? 'none' : 'var(--ring)',
            }}>
              <div style={{ fontSize: 14, fontWeight: 500, lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                {msg.content}
              </div>
              {msg.role === 'assistant' && (
                <div style={{ marginTop: 12, display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center' }}>
                  {msg.isInsight && (
                    <span className="badge badge-insight">
                      <AlertTriangle size={10} /> INSIGHT
                    </span>
                  )}
                  {msg.source && (
                    <span style={{
                      fontSize: 11, fontWeight: 500, padding: '3px 10px',
                      borderRadius: 'var(--radius-pill)', background: 'var(--color-canvas)',
                      color: 'rgba(16,19,14,0.5)',
                    }}>
                      via {msg.source}
                    </span>
                  )}
                </div>
              )}
              {msg.sql && (
                <details style={{ marginTop: 12 }}>
                  <summary style={{
                    fontSize: 12, fontWeight: 600, cursor: 'pointer',
                    color: 'rgba(16,19,14,0.45)', display: 'flex', alignItems: 'center', gap: 4,
                  }}>
                    <Code size={12} /> View SQL
                  </summary>
                  <pre style={{
                    marginTop: 8, padding: 12, background: 'var(--color-canvas)',
                    borderRadius: 'var(--radius-sm)', fontSize: 12, fontFamily: 'monospace',
                    overflow: 'auto', lineHeight: 1.5, color: 'var(--color-ink)',
                  }}>
                    {msg.sql}
                  </pre>
                </details>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
            <div style={{
              width: 32, height: 32, borderRadius: '50%', flexShrink: 0,
              background: 'var(--color-sage-tint)', display: 'flex',
              alignItems: 'center', justifyContent: 'center',
            }}>
              <Bot size={16} style={{ color: 'var(--color-forest)' }} />
            </div>
            <div className="card" style={{ padding: '14px 18px' }}>
              <div style={{ display: 'flex', gap: 4 }}>
                {[0, 1, 2].map(i => (
                  <div key={i} style={{
                    width: 8, height: 8, borderRadius: '50%',
                    background: 'var(--color-brand-lime)',
                    animation: `skeleton-pulse 1.4s ${i * 0.2}s ease-in-out infinite`,
                  }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{ display: 'flex', gap: 12, paddingTop: 16, borderTop: '1px solid var(--color-line)' }}>
        <input
          className="search-input"
          placeholder="Ask a question about the insurance data..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSubmit()}
          disabled={loading}
        />
        <button
          className="btn btn-primary"
          onClick={() => handleSubmit()}
          disabled={loading || !input.trim()}
          style={{ opacity: loading || !input.trim() ? 0.5 : 1 }}
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  )
}
