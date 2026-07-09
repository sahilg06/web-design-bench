import React, { useState } from 'react';

const PLANS = [
  {
    name: 'Starter',
    priceMonthly: 0,
    priceAnnual: 0,
    tagline: 'For solo builders and side projects',
    features: [
      '3 active workflows',
      '5,000 events / month',
      '25+ core integrations',
      'Community support',
      '7-day execution logs',
    ],
    cta: 'Start for free',
    highlighted: false,
  },
  {
    name: 'Pro',
    priceMonthly: 49,
    priceAnnual: 39,
    tagline: 'For growing teams shipping automations',
    features: [
      'Unlimited workflows',
      '250,000 events / month',
      '400+ integrations',
      'Priority chat support',
      '90-day execution logs',
      'Version control & rollback',
      'Custom code steps (JS/Python)',
      'Team roles & permissions',
    ],
    cta: 'Start 14-day trial',
    highlighted: true,
    badge: 'Most popular',
  },
  {
    name: 'Enterprise',
    priceMonthly: null,
    priceAnnual: null,
    tagline: 'For orgs at scale with compliance needs',
    features: [
      'Unlimited events',
      'Dedicated infrastructure',
      'SSO, SAML, SCIM',
      '24/7 dedicated CSM',
      'Unlimited retention',
      'Custom SLAs (99.99%+)',
      'Private cloud & on-prem',
      'HIPAA, FedRAMP, ISO 27001',
    ],
    cta: 'Talk to sales',
    highlighted: false,
  },
];

const COMPARE = [
  { section: 'Platform', rows: [
    { f: 'Active workflows', s: '3', p: 'Unlimited', e: 'Unlimited' },
    { f: 'Monthly events', s: '5,000', p: '250,000', e: 'Unlimited' },
    { f: 'Data retention', s: '7 days', p: '90 days', e: 'Unlimited' },
  ]},
  { section: 'Integrations', rows: [
    { f: 'Pre-built connectors', s: '25+', p: '400+', e: '400+' },
    { f: 'Custom API builder', s: false, p: true, e: true },
    { f: 'Private connectors', s: false, p: false, e: true },
  ]},
  { section: 'Security & Compliance', rows: [
    { f: 'SOC 2 Type II', s: true, p: true, e: true },
    { f: 'HIPAA BAA', s: false, p: false, e: true },
    { f: 'SSO / SAML / SCIM', s: false, p: false, e: true },
    { f: 'Customer-managed keys', s: false, p: false, e: true },
  ]},
];

function Check({ on }) {
  if (on === true) return <span className="text-accent font-bold">●</span>;
  if (on === false) return <span className="text-borderc">—</span>;
  return <span className="text-white font-semibold text-sm">{on}</span>;
}

export default function Pricing() {
  const [annual, setAnnual] = useState(true);

  return (
    <div className="relative overflow-hidden">
      {/* HERO */}
      <section className="relative">
        <div className="absolute inset-0 bg-grid opacity-30"></div>
        <div className="absolute -top-20 left-1/2 -translate-x-1/2 h-96 w-[700px] rounded-full bg-accent/20 blur-3xl"></div>
        <div className="relative max-w-4xl mx-auto px-5 sm:px-8 pt-20 pb-8 text-center">
          <span className="text-xs font-bold tracking-widest text-accent uppercase">Pricing</span>
          <h1 className="mt-3 text-4xl md:text-6xl font-black tracking-tight text-white">
            Simple pricing.{' '}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-accent to-accentWarm">Serious scale.</span>
          </h1>
          <p className="mt-5 text-lg text-textSecondary">
            Start free. Upgrade when you're ready. Every plan includes unlimited seats and our core integration library.
          </p>

          {/* Toggle */}
          <div className="mt-8 inline-flex items-center gap-3 p-1 rounded-full bg-surface border border-borderc">
            <button
              onClick={() => setAnnual(false)}
              className={`px-5 py-2 rounded-full text-sm font-semibold transition ${
                !annual ? 'bg-white text-slate-900 shadow-lg' : 'text-textSecondary hover:text-white'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setAnnual(true)}
              className={`px-5 py-2 rounded-full text-sm font-semibold transition flex items-center gap-2 ${
                annual ? 'bg-white text-slate-900 shadow-lg' : 'text-textSecondary hover:text-white'
              }`}
            >
              Annual
              <span className="px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-accent/20 text-accent">Save 20%</span>
            </button>
          </div>
        </div>
      </section>

      {/* PLANS */}
      <section className="max-w-7xl mx-auto px-5 sm:px-8 pb-16 pt-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
          {PLANS.map((p) => {
            const price = annual ? p.priceAnnual : p.priceMonthly;
            return (
              <div
                key={p.name}
                className={`relative rounded-2xl p-7 md:p-8 flex flex-col ${
                  p.highlighted
                    ? 'bg-gradient-to-br from-surface via-surface to-background border-2 border-accent glow-pulse md:-mt-4 md:mb-4'
                    : 'bg-surface/60 border border-borderc'
                }`}
              >
                {p.badge && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full text-[10px] font-bold tracking-widest uppercase text-slate-900 bg-gradient-to-r from-accent to-accentWarm shadow-lg">
                    {p.badge}
                  </span>
                )}
                <div>
                  <h3 className="text-2xl font-black text-white">{p.name}</h3>
                  <p className="mt-1 text-sm text-textSecondary">{p.tagline}</p>

                  <div className="mt-6 flex items-baseline gap-1.5">
                    {price === null ? (
                      <span className="text-4xl font-black text-white">Custom</span>
                    ) : (
                      <>
                        <span className="text-5xl font-black text-white">${price}</span>
                        <span className="text-textSecondary text-sm">/ user / mo</span>
                      </>
                    )}
                  </div>
                  {annual && price !== null && price > 0 && (
                    <p className="mt-1 text-xs text-textSecondary">Billed annually · Save ${(p.priceMonthly - p.priceAnnual) * 12}/user/yr</p>
                  )}
                </div>

                <button
                  className={`mt-6 w-full py-3 rounded-xl font-semibold transition ${
                    p.highlighted
                      ? 'text-slate-900 bg-gradient-to-r from-accent to-accentWarm hover:brightness-110 shadow-lg shadow-accent/30'
                      : 'text-white bg-background border border-borderc hover:border-accent'
                  }`}
                >
                  {p.cta}
                </button>

                <ul className="mt-7 space-y-3 flex-1">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2.5 text-sm">
                      <span className={`mt-0.5 h-5 w-5 rounded-full grid place-items-center shrink-0 ${
                        p.highlighted ? 'bg-accent text-slate-900' : 'bg-surface border border-borderc text-accent'
                      }`}>
                        <svg viewBox="0 0 12 12" className="h-3 w-3" fill="none" stroke="currentColor" strokeWidth="2.5">
                          <path d="M2 6l3 3 5-6" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </span>
                      <span className="text-textPrimary">{f}</span>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
      </section>

      {/* COMPARISON */}
      <section className="max-w-6xl mx-auto px-5 sm:px-8 py-16">
        <h2 className="text-3xl md:text-4xl font-black text-white text-center">Compare every feature</h2>
        <p className="mt-3 text-center text-textSecondary">A closer look at what each plan includes.</p>

        <div className="mt-10 rounded-2xl bg-surface/40 border border-borderc overflow-hidden">
          <div className="grid grid-cols-4 items-center px-5 py-4 border-b border-borderc bg-background/40">
            <div className="text-xs font-bold tracking-widest text-textSecondary uppercase">Feature</div>
            <div className="text-sm font-bold text-white text-center">Starter</div>
            <div className="text-sm font-bold text-accent text-center">Pro</div>
            <div className="text-sm font-bold text-white text-center">Enterprise</div>
          </div>
          {COMPARE.map((sec) => (
            <div key={sec.section}>
              <div className="px-5 py-3 bg-background/30 border-t border-borderc/60">
                <span className="text-xs font-bold tracking-widest text-accent uppercase">{sec.section}</span>
              </div>
              {sec.rows.map((r) => (
                <div key={r.f} className="grid grid-cols-4 items-center px-5 py-4 border-t border-borderc/60">
                  <div className="text-sm text-textPrimary">{r.f}</div>
                  <div className="text-center"><Check on={r.s} /></div>
                  <div className="text-center bg-accent/5"><Check on={r.p} /></div>
                  <div className="text-center"><Check on={r.e} /></div>
                </div>
              ))}
            </div>
          ))}
        </div>
      </section>

      {/* FAQ */}
      <section className="max-w-4xl mx-auto px-5 sm:px-8 py-16">
        <h2 className="text-3xl md:text-4xl font-black text-white text-center">Pricing FAQ</h2>
        <div className="mt-10 space-y-3">
          {[
            {
              q: 'What counts as an event?',
              a: 'An event is any trigger, step, or action inside a workflow — from a webhook fired by Stripe to a Slack message you sent. Retries and internal branching steps are not counted.',
            },
            {
              q: 'Can I change plans later?',
              a: 'Absolutely. Upgrades take effect immediately with prorated billing; downgrades apply at the end of your current cycle. No penalties either way.',
            },
            {
              q: 'Do you offer discounts for startups or nonprofits?',
              a: 'Yes — we offer 50% off Pro for eligible early-stage startups (via our Nexus for Startups program) and 100% off for registered 501(c)(3) nonprofits.',
            },
            {
              q: 'What happens if I exceed my event limit?',
              a: 'Your workflows keep running. Overage events are billed at $0.0008 each, and we notify you at 80% consumption so there are no surprises at month-end.',
            },
            {
              q: 'Is there an on-premise option?',
              a: 'Enterprise customers can deploy Nexus into their own VPC (AWS, GCP, Azure) or fully air-gapped on-prem environments with our Federal edition.',
            },
          ].map((f, i) => (
            <details key={i} className="group rounded-xl bg-surface/60 border border-borderc p-5 open:border-accent transition">
              <summary className="cursor-pointer list-none flex items-start justify-between gap-4">
                <span className="text-base font-semibold text-white">{f.q}</span>
                <span className="text-accent text-xl leading-none group-open:rotate-45 transition-transform">+</span>
              </summary>
              <p className="mt-3 text-textSecondary leading-relaxed">{f.a}</p>
            </details>
          ))}
        </div>
      </section>
    </div>
  );
}
