import { useState } from 'react';

const FEATURES = {
  cloud: [
    {
      icon: '⚡',
      title: 'Global Inference API',
      desc: 'Route requests through 40+ edge regions with automatic failover. 99.99% uptime SLA backed by real credits.',
      tag: 'API',
    },
    {
      icon: '📊',
      title: 'Realtime Analytics',
      desc: 'Track token usage, latency, error rates, and cost per endpoint in a single unified dashboard.',
      tag: 'Observability',
    },
    {
      icon: '🔄',
      title: 'Auto-scaling Workers',
      desc: 'From 10 to 10 million requests per minute — capacity scales elastically with predictable pricing.',
      tag: 'Infrastructure',
    },
    {
      icon: '🎯',
      title: 'Model Fine-tuning',
      desc: 'Upload your dataset and get a specialized model in under 20 minutes. Zero DevOps required.',
      tag: 'Training',
    },
    {
      icon: '🔗',
      title: 'Native Integrations',
      desc: 'Prebuilt connectors for Salesforce, Snowflake, Slack, HubSpot, and 60+ other business tools.',
      tag: 'Integrations',
    },
    {
      icon: '🧪',
      title: 'A/B Experimentation',
      desc: 'Compare models, prompts, and versions side-by-side with statistical significance testing built in.',
      tag: 'Testing',
    },
  ],
  onprem: [
    {
      icon: '🏢',
      title: 'Air-gapped Deployment',
      desc: 'Deploy Luminary entirely within your VPC or physical datacenter. Zero external network dependencies.',
      tag: 'Deployment',
    },
    {
      icon: '🛡️',
      title: 'Hardware-level Isolation',
      desc: 'Dedicated GPU clusters with SGX enclaves. Your data and models remain isolated at every layer.',
      tag: 'Security',
    },
    {
      icon: '🔐',
      title: 'Enterprise SSO',
      desc: 'SAML 2.0, OIDC, LDAP, and Active Directory integration with per-team role-based access controls.',
      tag: 'Identity',
    },
    {
      icon: '📜',
      title: 'Full Audit Logging',
      desc: 'Every prompt, response, and admin action logged to SIEM-compatible immutable storage.',
      tag: 'Compliance',
    },
    {
      icon: '⚙️',
      title: 'Custom Model Registry',
      desc: 'Bring your own weights or fine-tune inside your environment. Full ownership of trained IP.',
      tag: 'Models',
    },
    {
      icon: '📞',
      title: 'Dedicated Support',
      desc: '24/7 named-engineer support with 15-minute response SLA. Quarterly on-site architecture reviews.',
      tag: 'Support',
    },
  ],
};

export default function Features() {
  const [mode, setMode] = useState('cloud');

  return (
    <>
      <div className="section-header">
        <div className="section-eyebrow">Platform</div>
        <h2>Everything you need to ship AI to production</h2>
        <p>
          A complete toolkit for building, deploying, and scaling machine learning
          applications — whether you run in the cloud or behind your firewall.
        </p>
      </div>

      <div className="toggle-wrap">
        <div className="toggle" role="tablist" aria-label="Deployment mode">
          <button
            className={`toggle-btn ${mode === 'cloud' ? 'active' : ''}`}
            onClick={() => setMode('cloud')}
            role="tab"
            aria-selected={mode === 'cloud'}
          >
            ☁ Cloud
          </button>
          <button
            className={`toggle-btn ${mode === 'onprem' ? 'active' : ''}`}
            onClick={() => setMode('onprem')}
            role="tab"
            aria-selected={mode === 'onprem'}
          >
            🏢 On-Premise
          </button>
        </div>
      </div>

      <div className="features-grid">
        {FEATURES[mode].map((feature) => (
          <article key={feature.title} className="feature-card">
            <div className="feature-icon">{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.desc}</p>
            <span className="feature-tag">{feature.tag}</span>
          </article>
        ))}
      </div>
    </>
  );
}
