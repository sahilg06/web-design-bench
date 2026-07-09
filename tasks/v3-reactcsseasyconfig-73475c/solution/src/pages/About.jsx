const TEAM = [
  {
    initials: 'SC',
    name: 'Sarah Chen',
    role: 'Co-founder & CEO',
    bio: 'Previously led ML infrastructure at Stripe. MIT PhD in distributed systems. Believes production AI should be boring — in the best possible way.',
    photoClass: '',
  },
  {
    initials: 'DR',
    name: 'David Ramírez',
    role: 'Co-founder & CTO',
    bio: 'Former principal engineer at Anthropic and Google Brain. Author of three widely-cited papers on inference optimization and model serving at scale.',
    photoClass: 'p2',
  },
  {
    initials: 'AK',
    name: 'Aisha Kapoor',
    role: 'Chief Product Officer',
    bio: 'Built enterprise data products at Snowflake and Databricks. Passionate about designing tools that developers genuinely love using every day.',
    photoClass: 'p3',
  },
];

export default function About() {
  return (
    <>
      <section className="about-hero">
        <div className="section-eyebrow">Our Story</div>
        <h1>Making AI infrastructure invisible</h1>
        <p>
          Luminary was founded in 2022 by a team of engineers who spent years wiring
          up brittle ML pipelines at hyperscalers. We built the platform we wished
          existed — one where deploying AI feels less like plumbing and more like
          shipping product.
        </p>
      </section>

      <div className="mission-card">
        <div className="mission-eyebrow">Our Mission</div>
        <h2>Intelligence should be as accessible as electricity</h2>
        <p>
          Every meaningful technological shift eventually disappears into the fabric
          of everyday work. Electricity, the internet, the cloud — none of them
          require a specialist to be useful. We're building the same standard for AI:
          a platform where any team, at any scale, can turn ideas into intelligent
          systems without spending months on infrastructure. When AI becomes boring,
          it becomes powerful. That's the future we're building toward.
        </p>
      </div>

      <div className="section-header">
        <div className="section-eyebrow">Leadership</div>
        <h2>Meet the team</h2>
        <p>
          A small, experienced group with deep roots in production ML, distributed
          systems, and enterprise software.
        </p>
      </div>

      <div className="team-grid">
        {TEAM.map((member) => (
          <article key={member.name} className="team-card">
            <div className={`team-photo ${member.photoClass}`}>{member.initials}</div>
            <div className="team-info">
              <div className="team-name">{member.name}</div>
              <div className="team-role">{member.role}</div>
              <p className="team-bio">{member.bio}</p>
            </div>
          </article>
        ))}
      </div>

      <div className="stats-row">
        <div className="stat-item">
          <div className="stat-num">400+</div>
          <div className="stat-label">Enterprise customers</div>
        </div>
        <div className="stat-item">
          <div className="stat-num">14B</div>
          <div className="stat-label">Requests per month</div>
        </div>
        <div className="stat-item">
          <div className="stat-num">40+</div>
          <div className="stat-label">Global regions</div>
        </div>
        <div className="stat-item">
          <div className="stat-num">99.99%</div>
          <div className="stat-label">Platform uptime</div>
        </div>
      </div>
    </>
  );
}
