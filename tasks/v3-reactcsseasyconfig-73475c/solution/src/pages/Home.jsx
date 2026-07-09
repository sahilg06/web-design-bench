export default function Home({ onNavigate }) {
  return (
    <>
      <section className="hero">
        <div className="hero-badge">
          <span className="hero-badge-dot"></span>
          <span>Now with Luminary v4.2 — 3× faster inference</span>
        </div>
        <h1>Intelligence Simplified</h1>
        <p className="hero-subtitle">
          The enterprise AI platform that turns complex data into decisive action.
          Deploy production-ready models in minutes, not months — with the reliability
          your team already expects.
        </p>
        <div className="hero-actions">
          <button className="btn btn-primary btn-lg" onClick={() => onNavigate('page_contact')}>
            Start Free Trial
          </button>
          <button className="btn btn-secondary btn-lg" onClick={() => onNavigate('page_features')}>
            View Live Demo
          </button>
        </div>

        <div className="hero-mockup" aria-hidden="true">
          <div className="mockup-header">
            <span className="mockup-dot"></span>
            <span className="mockup-dot"></span>
            <span className="mockup-dot"></span>
          </div>
          <div className="mockup-grid">
            <div className="mockup-stat">
              <div className="mockup-stat-label">Requests / min</div>
              <div className="mockup-stat-value">14,208</div>
              <div className="mockup-stat-trend">↑ 12.4%</div>
            </div>
            <div className="mockup-stat">
              <div className="mockup-stat-label">Avg Latency</div>
              <div className="mockup-stat-value">42ms</div>
              <div className="mockup-stat-trend">↓ 8.1%</div>
            </div>
            <div className="mockup-stat">
              <div className="mockup-stat-label">Accuracy</div>
              <div className="mockup-stat-value">99.7%</div>
              <div className="mockup-stat-trend">↑ 0.3%</div>
            </div>
            <div className="mockup-stat">
              <div className="mockup-stat-label">Uptime</div>
              <div className="mockup-stat-value">99.99%</div>
              <div className="mockup-stat-trend">30-day</div>
            </div>
            <div className="mockup-chart">
              {[45, 62, 38, 78, 55, 88, 72, 95, 68, 82, 91, 76].map((h, i) => (
                <div key={i} className="mockup-bar" style={{ height: `${h}%` }}></div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <div className="section-eyebrow">Why Luminary</div>
          <h2>Built for teams that demand more</h2>
          <p>
            Three principles guide everything we build — because enterprise AI shouldn't
            require compromise.
          </p>
        </div>

        <div className="value-grid">
          <div className="value-card">
            <div className="value-icon">⚡</div>
            <h3>Speed</h3>
            <p>
              Sub-50ms inference at global scale. Our proprietary caching layer and
              edge routing deliver responses 3× faster than the industry benchmark,
              even under peak load.
            </p>
          </div>
          <div className="value-card">
            <div className="value-icon">◎</div>
            <h3>Accuracy</h3>
            <p>
              99.7% precision on production workloads. Continuous fine-tuning pipelines
              and human-in-the-loop validation ensure models improve every day —
              automatically.
            </p>
          </div>
          <div className="value-card">
            <div className="value-icon">🔒</div>
            <h3>Security</h3>
            <p>
              SOC 2 Type II, HIPAA, and ISO 27001 certified. Data never leaves your
              region, encryption is end-to-end, and every request is fully audited
              by default.
            </p>
          </div>
        </div>
      </section>

      <section className="logo-strip">
        <div className="logo-strip-label">Trusted by 400+ leading organizations</div>
        <div className="logos">
          <div className="logo-item"><span className="logo-mark"></span>Northwind</div>
          <div className="logo-item"><span className="logo-mark"></span>Contoso</div>
          <div className="logo-item"><span className="logo-mark"></span>Meridian</div>
          <div className="logo-item"><span className="logo-mark"></span>Halcyon</div>
          <div className="logo-item"><span className="logo-mark"></span>Ironclad</div>
          <div className="logo-item"><span className="logo-mark"></span>Vantage</div>
        </div>
      </section>
    </>
  );
}
