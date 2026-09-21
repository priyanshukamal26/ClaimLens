import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, Activity, Globe, CheckCircle2, ArrowRight } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      {/* 1. NAVBAR */}
      <nav className="landing-nav">
        <div className="nav-container">
          <div className="nav-left">
            <div className="brand-logo">CL</div>
            <span className="brand-name">ClaimLens</span>
          </div>
          <div className="nav-center">
            <a href="#features">Features</a>
            <a href="#architecture">Architecture</a>
            <a href="#security">Security</a>
          </div>
          <div className="nav-right">
            <button className="nav-link-btn">Log in</button>
            <button className="nav-cta-btn" onClick={() => navigate('/app/overview')}>
              Go to Dashboard
            </button>
          </div>
        </div>
      </nav>

      {/* 2. HERO SECTION */}
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <h1 className="hero-title">
              Fraud detection for here, there and everywhere.
            </h1>
            <p className="hero-subtitle">
              ClaimLens Nexus uses a 3-layer anomaly detection pipeline to surface insights. Never decisions. 
              Join the modern standard for Indian insurance analytics.
            </p>
            <div className="hero-actions">
              <button className="primary-btn" onClick={() => navigate('/app/overview')}>
                See it in action
              </button>
              <button className="secondary-btn">Read the docs</button>
            </div>
          </div>
          <div className="hero-widget-container">
            {/* Wise-style interactive widget mock */}
            <div className="hero-widget">
              <div className="widget-header">
                <h3>Risk Calculator Demo</h3>
                <span className="live-badge">● Live</span>
              </div>
              <div className="widget-body">
                <div className="input-group">
                  <label>Claim Amount</label>
                  <div className="input-field">
                    <span>₹</span>
                    <input type="text" value="2,45,000" readOnly />
                  </div>
                </div>
                <div className="calculation-steps">
                  <div className="step">
                    <span className="step-icon">1</span>
                    <span className="step-text">Rules Engine: Pass</span>
                  </div>
                  <div className="step">
                    <span className="step-icon">2</span>
                    <span className="step-text">Isolation Forest: 0.82 Anomaly</span>
                  </div>
                  <div className="step">
                    <span className="step-icon">3</span>
                    <span className="step-text">Louvain Graph: Suspicious Ring</span>
                  </div>
                </div>
                <div className="widget-result">
                  <div className="result-label">Combined Score</div>
                  <div className="result-value">0.89 <span style={{color: '#ff4d4f'}}>High Risk</span></div>
                </div>
                <button className="widget-btn" onClick={() => navigate('/app/review')}>
                  Review in Queue
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. SOCIAL PROOF */}
      <section className="social-proof">
        <div className="social-container">
          <p>Trusted to analyze claims for top simulated insurers</p>
          <div className="logo-grid">
            <div className="mock-logo">HDFC ERGO</div>
            <div className="mock-logo">ICICI Lombard</div>
            <div className="mock-logo">Star Health</div>
            <div className="mock-logo">Bajaj Allianz</div>
            <div className="mock-logo">SBI General</div>
          </div>
        </div>
      </section>

      {/* 4. VALUE PROP GRID */}
      <section className="value-props" id="features">
        <div className="grid-container">
          <div className="grid-item">
            <div className="icon-wrapper"><Activity size={24} /></div>
            <h3>Real-time Analytics</h3>
            <p>Powered by DuckDB in-memory engine, analyzing 8,000+ claims instantly without database overhead.</p>
          </div>
          <div className="grid-item">
            <div className="icon-wrapper"><ShieldAlert size={24} /></div>
            <h3>3-Layer Detection</h3>
            <p>Rules engine, Scikit-Learn Isolation Forest, and NetworkX Graph Community detection working in unison.</p>
          </div>
          <div className="grid-item">
            <div className="icon-wrapper"><CheckCircle2 size={24} /></div>
            <h3>Secure Sandbox</h3>
            <p>External access disabled. All queries guarded by sqlglot parsing. Your data never leaves the premises.</p>
          </div>
        </div>
      </section>

      {/* 5. ZIG ZAG HIGHLIGHTS */}
      <section className="highlights" id="architecture">
        <div className="highlight-row">
          <div className="highlight-text">
            <h2>Meet Ask ClaimLens.</h2>
            <p>
              Your personal AI data analyst. Ask questions in plain English, and our 4-stage LLM fallback chain 
              writes the DuckDB SQL, verifies it against a strict allowlist, and narrates the results.
            </p>
            <ul className="feature-list">
              <li><CheckCircle2 size={16} /> Groq (Llama 3) for speed</li>
              <li><CheckCircle2 size={16} /> Gemini 1.5 Pro fallback</li>
              <li><CheckCircle2 size={16} /> Strict SQL Guarding</li>
            </ul>
            <button className="link-btn mt-6" style={{color: 'var(--color-brand-lime)', marginTop: 24}}>Explore the Architecture <ArrowRight size={16} /></button>
          </div>
          <div className="highlight-image">
            <div className="mock-ui">
              <div className="mock-header">Ask ClaimLens</div>
              <div className="mock-chat">
                <div className="user-msg">What is the loss ratio for Motor in Maharashtra?</div>
                <div className="ai-msg">
                  <div className="sql-box">SELECT ROUND(SUM(c.claim_amount) / SUM(p.premium_amount) * 100, 2) ...</div>
                  The data shows a loss ratio of 82.4% for Motor policies in Maharashtra.
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="highlight-row reverse">
          <div className="highlight-text">
            <h2>Insights, never decisions.</h2>
            <p>
              We believe AI should surface insights, but humans make the decisions. 
              The Review Queue ranks anomalies, but the Decision Log acts as an immutable ledger of human action.
            </p>
            <ul className="feature-list">
              <li><CheckCircle2 size={16} /> Immutable Decision Ledger</li>
              <li><CheckCircle2 size={16} /> Transparent scoring breakdown</li>
              <li><CheckCircle2 size={16} /> Clear accountability</li>
            </ul>
          </div>
          <div className="highlight-image">
            <div className="mock-ui dark">
              <div className="mock-row" style={{display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: 12}}>
                <span>CLM-8924</span>
                <span style={{background: 'rgba(255, 235, 59, 0.2)', color: '#ffee58', padding: '4px 8px', borderRadius: 12, fontSize: 12}}>Score: 0.89</span>
              </div>
              <div className="mock-row" style={{display: 'flex', justifyContent: 'space-between', paddingTop: 12}}>
                <span>CLM-2104</span>
                <span style={{background: 'rgba(255, 235, 59, 0.2)', color: '#ffee58', padding: '4px 8px', borderRadius: 12, fontSize: 12}}>Score: 0.76</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. GLOBAL BANNER */}
      <section className="global-banner" id="security">
        <div className="global-content">
          <Globe size={48} style={{opacity: 0.8, marginBottom: 24}} />
          <h2>Ready to analyze claims across India?</h2>
          <p>Join the future of transparent, AI-assisted insurance operations.</p>
          <button className="primary-btn" style={{marginTop: 32}} onClick={() => navigate('/app/overview')}>
            Launch Dashboard
          </button>
        </div>
      </section>

      {/* 7. FOOTER */}
      <footer className="landing-footer">
        <div className="footer-container">
          <div className="footer-top">
            <div className="footer-brand">
              <div className="brand-logo small">CL</div>
              <span className="brand-name">ClaimLens</span>
            </div>
          </div>
          <div className="footer-links">
            <div className="link-column">
              <h4>Company</h4>
              <a href="#">About us</a>
              <a href="#">Careers</a>
              <a href="#">Press</a>
            </div>
            <div className="link-column">
              <h4>Product</h4>
              <a href="#">Executive Overview</a>
              <a href="#">Review Queue</a>
              <a href="#">Ask ClaimLens</a>
            </div>
            <div className="link-column">
              <h4>Resources</h4>
              <a href="#">Documentation</a>
              <a href="#">Architecture</a>
              <a href="#">Security</a>
            </div>
            <div className="link-column">
              <h4>Legal</h4>
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
              <a href="#">Cookie Policy</a>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2026 ClaimLens Nexus. All rights reserved.</p>
            <p className="disclaimer">
              For demonstration purposes only. Synthetic data does not represent real individuals or organizations.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
