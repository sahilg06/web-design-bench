const TEAM = [
  { name: 'Elena Marchetti', role: 'Founder & Creative Director', tone: 'tone-coral' },
  { name: 'Jonas Okafor',    role: 'Head of Design',              tone: 'tone-indigo' },
  { name: 'Priya Ramanathan', role: 'Design Engineering Lead',    tone: 'tone-mint' },
  { name: 'Marcus Reyes',    role: 'Strategy Director',           tone: 'tone-plum' },
];

const AWARDS = [
  { year: '2025', title: 'Awwwards Site of the Year', desc: 'Recognized for the Northline Banking product redesign.' },
  { year: '2024', title: 'Brand New — Notable Rebrand', desc: 'Vessel Coffee Co. identity system, spring collection.' },
  { year: '2023', title: 'Type Directors Club Cert.', desc: 'Custom display face designed for Meridian Wellness.' },
];

const VALUES = [
  {
    title: 'Craft',
    tone: 'tone-coral',
    icon: 'C',
    desc: 'Every kern, every curve, every millisecond of motion is intentional. The details are the design.',
  },
  {
    title: 'Collaboration',
    tone: 'tone-indigo',
    icon: 'Co',
    desc: 'We work as one team with our partners — shared docs, shared decisions, shared credit for the outcome.',
  },
  {
    title: 'Innovation',
    tone: 'tone-mint',
    icon: 'I',
    desc: 'We ship tomorrow-first. New tools, new mediums, new questions — every project pushes the studio forward.',
  },
];

export default function About(props) {
  return (
    <>
      <section class="page-intro">
        <div class="container">
          <span class="eyebrow">About the Studio</span>
          <h1>An independent design practice, since 2018.</h1>
          <p>
            Aura Creative is a fifteen-person studio in Williamsburg, Brooklyn.
            We work in tight, senior-led teams for a small number of partners
            each year.
          </p>
        </div>
      </section>

      <section class="section" style="padding-top: 2rem;">
        <div class="container">
          <div class="about-story">
            <div class="about-story-image tone-plum"></div>
            <div class="about-story-copy">
              <span class="eyebrow">Our Story</span>
              <h2 class="section-heading">Founded on a small, stubborn idea.</h2>
              <p>
                Aura began in the winter of 2018, when Elena Marchetti left a
                global agency to start a studio built around a stubborn idea:
                that the best design work happens when the people making it are
                also the people talking to the client, sketching the strategy,
                and shipping the last kilobyte.
              </p>
              <p>
                Seven years later, we've grown to fifteen people — designers,
                engineers, strategists, and writers — and we still work that
                way. No account layer. No hand-offs. Just senior craftspeople
                doing the work.
              </p>
              <button
                class="btn btn-ghost btn-arrow"
                onClick={() => props.go('page_work')}
              >
                See what we've built
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Team */}
      <section class="section">
        <div class="container">
          <span class="eyebrow">The Team</span>
          <h2 class="section-heading">Small studio, senior team.</h2>
          <p class="section-sub">
            Every project is led by someone whose name is on the door. Meet a
            few of the people you'll actually work with.
          </p>

          <div class="team-grid">
            {TEAM.map((m) => (
              <div class="team-card">
                <div class={`team-avatar ${m.tone}`}></div>
                <div class="team-name">{m.name}</div>
                <div class="team-role">{m.role}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Awards */}
      <section class="section" style="padding-top: 0;">
        <div class="container">
          <span class="eyebrow">Recognition</span>
          <h2 class="section-heading">Some kind words from our peers.</h2>
          <p class="section-sub">
            We don't chase awards — but we're grateful when the industry stops
            to notice the work.
          </p>

          <div class="awards-list">
            {AWARDS.map((a) => (
              <div class="award-card">
                <div class="award-year">{a.year}</div>
                <div class="award-title">{a.title}</div>
                <p class="award-desc">{a.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Values */}
      <section class="section" style="padding-top: 0;">
        <div class="container">
          <span class="eyebrow">Our Values</span>
          <h2 class="section-heading">Three words we keep close.</h2>

          <div class="values-grid">
            {VALUES.map((v) => (
              <div class="value-card">
                <div class={`value-icon ${v.tone}`}>{v.icon}</div>
                <div class="value-title">{v.title}</div>
                <p class="value-desc">{v.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
