const SERVICES = [
  {
    icon: 'B',
    title: 'Brand Identity',
    desc: 'Naming, visual systems, typography, and the strategy that grounds them. Built to scale from launch to legacy.',
    price: 'From $18k · 6–10 weeks',
    tone: 'tone-coral',
  },
  {
    icon: 'W',
    title: 'Web Design',
    desc: 'Marketing sites and product surfaces engineered for speed, clarity, and conversion. Every pixel earns its place.',
    price: 'From $24k · 8–12 weeks',
    tone: 'tone-indigo',
  },
  {
    icon: 'M',
    title: 'Mobile Apps',
    desc: 'Native and cross-platform product design from first sketch to app store. We ship, then keep sharpening.',
    price: 'From $42k · 12–20 weeks',
    tone: 'tone-mint',
  },
  {
    icon: 'P',
    title: 'Print & Packaging',
    desc: 'Books, editorial systems, and physical goods that turn touchpoints into memories worth keeping.',
    price: 'From $12k · 4–8 weeks',
    tone: 'tone-mustard',
  },
];

const PROCESS = [
  { n: '01', title: 'Discovery',  desc: 'Immersion workshops, audits, and a written strategy brief before a single pixel moves.' },
  { n: '02', title: 'Design',     desc: 'Concept exploration, systematization, and rapid iteration against a small set of directions.' },
  { n: '03', title: 'Develop',    desc: 'Engineering builds in parallel with design — tokens, components, and interactions in a shared source of truth.' },
  { n: '04', title: 'Launch',     desc: 'Coordinated rollout, telemetry, and a 90-day partnership window to refine what matters.' },
];

const TECH = [
  'Figma', 'Framer', 'Webflow', 'Next.js', 'Solid JS', 'Swift', 'Kotlin',
  'Contentful', 'Sanity', 'Shopify', 'InDesign', 'After Effects',
];

export default function Services(props) {
  return (
    <>
      <section class="page-intro">
        <div class="container">
          <span class="eyebrow">Services</span>
          <h1>Full-service design, minus the fluff.</h1>
          <p>
            Four practices, one integrated team. Every engagement is scoped
            around outcomes — not deliverables — with senior designers embedded
            end-to-end.
          </p>
        </div>
      </section>

      <section class="section" style="padding-top: 2rem;">
        <div class="container">
          <div class="services-grid">
            {SERVICES.map((s) => (
              <div class="service-card">
                <div class={`service-icon ${s.tone}`}>{s.icon}</div>
                <h3 class="service-title">{s.title}</h3>
                <p class="service-desc">{s.desc}</p>
                <div class="service-price">{s.price}</div>
              </div>
            ))}
          </div>

          {/* Process */}
          <div class="process">
            <span class="eyebrow">How We Work</span>
            <h2 class="section-heading">A four-step process, refined over 140+ engagements.</h2>
            <p class="section-sub">
              Predictable rhythms and clear checkpoints. You always know where
              a project is, what's next, and what we need from you.
            </p>

            <div class="timeline">
              {PROCESS.map((step) => (
                <div class="timeline-step">
                  <div class="timeline-num">{step.n}</div>
                  <h4>{step.title}</h4>
                  <p>{step.desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div class="divider-line"></div>

          {/* Tech */}
          <div>
            <span class="eyebrow">Tooling</span>
            <h2 class="section-heading">Technologies we ship with.</h2>
            <p class="section-sub">
              A pragmatic stack chosen for craft, longevity, and handoff. We're
              opinionated but not dogmatic — the right tool for the right brief.
            </p>
            <div class="tech-chips">
              {TECH.map((t) => (
                <span class="tech-chip">{t}</span>
              ))}
            </div>
          </div>

          <div style="margin-top: 4rem; text-align: center;">
            <button class="btn btn-primary btn-arrow" onClick={() => props.go('page_contact')}>
              Discuss a project
            </button>
          </div>
        </div>
      </section>
    </>
  );
}
