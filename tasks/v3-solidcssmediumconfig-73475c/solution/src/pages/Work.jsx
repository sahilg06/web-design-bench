import { createSignal } from 'solid-js';

const FILTERS = ['All', 'Branding', 'Web', 'Mobile', 'Print'];

const PROJECTS = [
  { title: 'Vessel Coffee Co.', category: 'Branding', tone: 'tone-coral' },
  { title: 'Northline Banking',  category: 'Web',      tone: 'tone-indigo' },
  { title: 'Meridian Wellness',  category: 'Print',    tone: 'tone-mint' },
  { title: 'Orbit Fitness App',  category: 'Mobile',   tone: 'tone-plum' },
  { title: 'Fold & Co. Studio',  category: 'Branding', tone: 'tone-mustard' },
  { title: 'Fieldnote Journal',  category: 'Web',      tone: 'tone-teal' },
];

export default function Work(props) {
  const [filter, setFilter] = createSignal('All');

  const visible = () =>
    filter() === 'All'
      ? PROJECTS
      : PROJECTS.filter((p) => p.category === filter());

  return (
    <>
      <section class="page-intro">
        <div class="container">
          <span class="eyebrow">Portfolio</span>
          <h1>Our Work</h1>
          <p>
            A cross-section of brands, products, and objects we've helped shape
            over the past few years — spanning early-stage startups to
            established institutions.
          </p>
        </div>
      </section>

      <section class="section" style="padding-top: 2rem;">
        <div class="container">
          <div class="filter-tabs" role="tablist">
            {FILTERS.map((f) => (
              <button
                class={`filter-tab ${filter() === f ? 'active' : ''}`}
                onClick={() => setFilter(f)}
              >
                {f}
              </button>
            ))}
          </div>

          <div class="work-grid">
            {visible().map((p) => (
              <article class="project-card">
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

          {/* Featured Case Study Spotlight */}
          <div class="spotlight">
            <div class="spotlight-image tone-indigo"></div>
            <div>
              <span class="eyebrow spotlight-eyebrow">Featured Case Study</span>
              <h2>Reimagining trust for Northline Banking.</h2>
              <p>
                A twelve-month partnership to redesign the flagship consumer
                banking experience from the ground up. We shipped a new visual
                system, an entirely rebuilt onboarding flow, and a native
                mobile app that lifted engagement by 3.4× within two quarters.
              </p>

              <div class="spotlight-stats">
                <div class="spotlight-stat">
                  <div class="num">+340%</div>
                  <div class="label">Engagement</div>
                </div>
                <div class="spotlight-stat">
                  <div class="num">4.9★</div>
                  <div class="label">App Store</div>
                </div>
                <div class="spotlight-stat">
                  <div class="num">−62%</div>
                  <div class="label">Drop-off</div>
                </div>
              </div>

              <button class="btn btn-primary btn-arrow" onClick={() => props.go('page_contact')}>
                Start a similar project
              </button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
