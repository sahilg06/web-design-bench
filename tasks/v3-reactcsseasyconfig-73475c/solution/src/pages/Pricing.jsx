const TIERS = [
  {
    name: 'Basic',
    price: 49,
    desc: 'For small teams and side projects getting started with AI.',
    features: [
      '500,000 API requests / month',
      '5 concurrent models',
      'Standard latency tier',
      'Email support (48h response)',
      'Basic analytics dashboard',
    ],
    cta: 'Start Free Trial',
    featured: false,
  },
  {
    name: 'Professional',
    price: 249,
    desc: 'For growing companies scaling AI across multiple products.',
    features: [
      '10 million API requests / month',
      'Unlimited concurrent models',
      'Priority latency (< 50ms)',
      'Chat support (4h response)',
      'Advanced analytics + A/B testing',
      'Custom model fine-tuning',
      'SOC 2 audit reports',
    ],
    cta: 'Start Free Trial',
    featured: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    desc: 'For regulated industries and mission-critical deployments.',
    features: [
      'Unlimited requests + custom SLA',
      'Dedicated GPU cluster',
      'On-premise or private cloud',
      '24/7 named-engineer support',
      'HIPAA / FedRAMP compliance',
      'Quarterly architecture reviews',
      'Custom contract & billing',
    ],
    cta: 'Contact Sales',
    featured: false,
  },
];

const COMPARISON = [
  ['Monthly API requests', '500K', '10M', 'Unlimited'],
  ['Concurrent models', '5', 'Unlimited', 'Unlimited'],
  ['Latency SLA', 'Standard', '< 50ms', '< 25ms'],
  ['Support response time', '48 hours', '4 hours', '15 minutes'],
  ['A/B experimentation', '—', '✓', '✓'],
  ['Custom fine-tuning', '—', '✓', '✓'],
  ['On-premise deployment', '—', '—', '✓'],
  ['HIPAA / FedRAMP', '—', '—', '✓'],
  ['Dedicated engineer', '—', '—', '✓'],
];

export default function Pricing() {
  return (
    <>
      <div className="section-header">
        <div className="section-eyebrow">Pricing</div>
        <h2>Simple, predictable, transparent</h2>
        <p>
          Choose the plan that fits your scale today. Upgrade or downgrade any time —
          no hidden fees, no surprise overages.
        </p>
      </div>

      <div className="pricing-grid">
        {TIERS.map((tier) => (
          <article
            key={tier.name}
            className={`pricing-card ${tier.featured ? 'featured' : ''}`}
          >
            {tier.featured && <div className="pricing-badge">Most Popular</div>}
            <div className="pricing-tier">{tier.name}</div>
            <div className="pricing-price">
              {typeof tier.price === 'number' ? (
                <>
                  <span className="pricing-amount">${tier.price}</span>
                  <span className="pricing-period">/ month</span>
                </>
              ) : (
                <span className="pricing-amount">{tier.price}</span>
              )}
            </div>
            <p className="pricing-desc">{tier.desc}</p>
            <ul className="pricing-features">
              {tier.features.map((feat) => (
                <li key={feat}>
                  <span className="pricing-check">✓</span>
                  <span>{feat}</span>
                </li>
              ))}
            </ul>
            <button className={`btn ${tier.featured ? 'btn-primary' : 'btn-secondary'}`}>
              {tier.cta}
            </button>
          </article>
        ))}
      </div>

      <div className="comparison-wrap">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Feature</th>
              <th>Basic</th>
              <th>Professional</th>
              <th>Enterprise</th>
            </tr>
          </thead>
          <tbody>
            {COMPARISON.map(([label, ...cols]) => (
              <tr key={label}>
                <td>{label}</td>
                {cols.map((col, i) => (
                  <td key={i} className={col === '✓' ? 'comparison-yes' : ''}>
                    {col}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
