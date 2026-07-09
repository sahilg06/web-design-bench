const FEATURED = [
  {
    title: 'Vessel Coffee Co.',
    category: 'Brand Identity',
    tone: 'tone-coral',
  },
  {
    title: 'Northline Banking',
    category: 'Web & Product',
    tone: 'tone-indigo',
  },
  {
    title: 'Meridian Wellness',
    category: 'Packaging',
    tone: 'tone-mint',
  },
];

const LOGOS = [
  'Nautilus', 'Fold & Co.', 'Klariti', 'Orbit Labs', 'Fieldnote', 'Hemisphere',
];

export default function Home(props) {
  return (
    <>
      {/* Hero */}
      <section class="hero">
        <div class="container hero-inner">
          <span class="eyebrow">Est. 2018 · Brooklyn, NY</span>
          <h1>
            Design <em>Without</em><br />Boundaries.
          </h1>
          <p class="hero-sub">
            We're an independent studio partnering with ambitious founders and
            forward brands to shape identities, digital products, and cultural
            artifacts that resonate for years — not seasons.
          </p>
          <div class="hero-actions">
            <button class="btn btn-primary btn-arrow" onClick={() => props.go('page_work')}>
              View Our Work
            </button>
            <button class="btn btn-secondary" onClick={() => props.go('page_contact')}>
              Start a Project
            </button>
          </div>

          <div class="hero-meta">
            <div class="hero-meta-item">
              <span class="num">142</span>
              <span class="label">Projects Shipped</span>
            </div>
            <div class="hero-meta-item">
              <span class="num">38</span>
              <span class="label">Global Partners</span>
            </div>
            <div class="hero-meta-item">
              <span class="num">17</span>
              <span class="label">Industry Awards</span>
            </div>
            <div class="hero-meta-item">
              <span class="num">98%</span>
              <span class="label">Client Retention</span>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Projects */}
      <section class="section">
        <div class="container">
          <span class="eyebrow">Selected Work</span>
          <h2 class="section-heading">Recent projects we're proud of.</h2>
          <p class="section-sub">
            Every engagement is a research-forward collaboration. Here are three
            we shipped recently that spanned strategy, identity, and product.
          </p>

          <div class="projects-grid">
            {FEATURED.map((p) => (
              <article class="project-card" onClick={() => props.go('page_work')}>
                <div class={`project-image ${p.tone}`}>
                  <div class="project-overlay">
                    <span class="overlay-title">{p.title}</span>
                    <span class="overlay-link">View Case Study →</span>
                  </div>
                </div>
                <div class="project-body">
                  <h3 class="project-title">{p.title}</h3>
                  <span class="project-tag">{p.category}</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Studio Philosophy Quote */}
      <section class="quote-section">
        <div class="container">
          <div class="quote-block">
            <div class="quote-mark">“</div>
            <p class="quote-text">
              We believe design is the quiet architecture behind every great
              brand — an act of attention, of restraint, and of care for the
              humans on the other side of the screen.
            </p>
            <div class="quote-author">Elena Marchetti</div>
            <div class="quote-role">Founder & Creative Director</div>
          </div>
        </div>
      </section>

      {/* Client Logos */}
      <section class="logos">
        <div class="container">
          <p class="logos-title">Trusted by teams building the next decade</p>
          <div class="logos-strip">
            {LOGOS.map((name) => (
              <span class="logo-item">{name}</span>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
