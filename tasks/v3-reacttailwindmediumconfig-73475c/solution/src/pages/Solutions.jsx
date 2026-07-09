import React from 'react';

const SOLUTIONS = [
  {
    tag: 'Healthcare',
    title: 'HIPAA-native workflows for provider networks',
    desc: 'Sync patient records across EHRs, lab systems, and billing platforms — with audit trails and PHI-safe transformations built in. Nexus is the connective tissue behind 240+ hospital networks and telehealth providers.',
    bullets: [
      'HL7, FHIR, and X12 support out of the box',
      'BAA-covered infrastructure across all tiers',
      'Field-level PHI masking and de-identification',
      'Zero-copy integrations with Epic, Cerner, Athena',
    ],
    stat: { k: 'Faster claim reconciliation', v: '6.4x' },
    palette: 'from-accent to-cyan-300',
    visual: 'healthcare',
  },
  {
    tag: 'Finance',
    title: 'Real-time reconciliation for fintech operations',
    desc: 'Move money, ledger entries, and compliance signals across banking rails without dropping a decimal. Trusted by neobanks, PSPs, and asset managers handling $180B in annual transaction volume.',
    bullets: [
      'ACH, SEPA, SWIFT, and card network connectors',
      'SOC 2 Type II & PCI DSS Level 1 certified',
      'Idempotent workflows with cryptographic receipts',
      'Regulatory reporting to FinCEN, FCA, MAS',
    ],
    stat: { k: 'Reconciliation lag', v: '<400ms' },
    palette: 'from-accentWarm to-fuchsia-400',
    visual: 'finance',
  },
  {
    tag: 'Retail',
    title: 'Omnichannel commerce for scaling brands',
    desc: 'Unify inventory, orders, and customer signals from Shopify, Amazon, physical POS, and your ERP. Deliver same-day fulfillment intelligence and personalized promotions at 250M+ SKU scale.',
    bullets: [
      'Native connectors for Shopify, BigCommerce, NetSuite',
      'Sub-second inventory reservation across channels',
      'Warehouse & 3PL orchestration templates',
      'Customer 360 event stream to any warehouse',
    ],
    stat: { k: 'Order cycle reduction', v: '−42%' },
    palette: 'from-emerald-400 to-teal-300',
    visual: 'retail',
  },
];

function Illustration({ kind, palette }) {
  if (kind === 'healthcare') {
    return (
      <div className="relative aspect-[4/3] rounded-2xl bg-surface border border-borderc overflow-hidden p-6">
        <div className={`absolute -top-16 -right-16 h-48 w-48 rounded-full bg-gradient-to-br ${palette} opacity-20 blur-2xl`}></div>
        <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase mb-3">Patient sync · live</div>
        <div className="space-y-2.5">
          {[
            { name: 'EHR · Epic', status: 'synced', pct: 100 },
            { name: 'Lab System · Quest', status: 'syncing', pct: 72 },
            { name: 'Billing · Athena', status: 'synced', pct: 100 },
            { name: 'Pharmacy · Surescripts', status: 'queued', pct: 34 },
          ].map((r) => (
            <div key={r.name} className="rounded-lg bg-background/60 border border-borderc p-3">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-medium text-white">{r.name}</span>
                <span className="text-[10px] text-textSecondary">{r.status}</span>
              </div>
              <div className="h-1.5 rounded-full bg-borderc/60 overflow-hidden">
                <div className={`h-full bg-gradient-to-r ${palette}`} style={{ width: `${r.pct}%` }}></div>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 flex items-center gap-2 text-[10px] text-textSecondary">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
          PHI encrypted · BAA active · Audit trail on
        </div>
      </div>
    );
  }

  if (kind === 'finance') {
    return (
      <div className="relative aspect-[4/3] rounded-2xl bg-surface border border-borderc overflow-hidden p-6">
        <div className={`absolute -top-16 -left-16 h-48 w-48 rounded-full bg-gradient-to-br ${palette} opacity-20 blur-2xl`}></div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase">Reconciliation feed</div>
            <div className="text-lg font-black text-white">$1,284,940.22</div>
          </div>
          <span className="px-2 py-1 rounded-md text-[10px] font-semibold text-emerald-300 bg-emerald-500/10 border border-emerald-500/30">MATCHED</span>
        </div>
        {/* Fake sparkline */}
        <svg viewBox="0 0 200 60" className="w-full h-16 mb-3">
          <defs>
            <linearGradient id="g1" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stopColor="#818cf8" stopOpacity="0.5" />
              <stop offset="1" stopColor="#818cf8" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path d="M0,40 L20,32 L40,38 L60,20 L80,28 L100,14 L120,22 L140,10 L160,18 L180,6 L200,12 L200,60 L0,60 Z" fill="url(#g1)" />
          <path d="M0,40 L20,32 L40,38 L60,20 L80,28 L100,14 L120,22 L140,10 L160,18 L180,6 L200,12" fill="none" stroke="#818cf8" strokeWidth="1.5" />
        </svg>
        <div className="space-y-1.5 font-mono text-[10px]">
          {[
            { t: '10:42:11', v: 'ACH_CREDIT', amt: '+ $4,210.00', ok: true },
            { t: '10:42:09', v: 'CARD_AUTH', amt: '+ $89.42', ok: true },
            { t: '10:42:07', v: 'SWIFT_MT103', amt: '+ $12,000.00', ok: true },
            { t: '10:42:04', v: 'REVERSAL', amt: '− $50.00', ok: false },
          ].map((r) => (
            <div key={r.t} className="flex items-center justify-between text-textSecondary">
              <span>{r.t} <span className="text-white/80 ml-1">{r.v}</span></span>
              <span className={r.ok ? 'text-emerald-300' : 'text-amber-300'}>{r.amt}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // retail
  return (
    <div className="relative aspect-[4/3] rounded-2xl bg-surface border border-borderc overflow-hidden p-6">
      <div className={`absolute -bottom-16 -right-16 h-48 w-48 rounded-full bg-gradient-to-br ${palette} opacity-20 blur-2xl`}></div>
      <div className="flex items-center justify-between mb-4">
        <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase">Inventory across channels</div>
        <span className="text-[10px] text-emerald-300">● LIVE</span>
      </div>
      <div className="grid grid-cols-3 gap-2 mb-4">
        {[
          { c: 'Shopify', v: '18,240' },
          { c: 'Amazon', v: '9,432' },
          { c: 'Retail POS', v: '5,180' },
        ].map((c) => (
          <div key={c.c} className="rounded-lg bg-background/60 border border-borderc p-2.5">
            <div className="text-[9px] text-textSecondary uppercase tracking-wider">{c.c}</div>
            <div className="text-sm font-bold text-white">{c.v}</div>
          </div>
        ))}
      </div>
      {/* Fake grid of SKUs */}
      <div className="grid grid-cols-8 gap-1">
        {Array.from({ length: 32 }).map((_, i) => (
          <div
            key={i}
            className={`aspect-square rounded ${
              i % 7 === 0 ? 'bg-amber-400/60' : i % 5 === 0 ? 'bg-red-400/40' : 'bg-emerald-400/50'
            }`}
          ></div>
        ))}
      </div>
      <div className="mt-4 flex items-center justify-between text-[10px]">
        <span className="flex items-center gap-1.5 text-textSecondary"><span className="h-2 w-2 rounded-sm bg-emerald-400/70"></span> In stock</span>
        <span className="flex items-center gap-1.5 text-textSecondary"><span className="h-2 w-2 rounded-sm bg-amber-400/70"></span> Low</span>
        <span className="flex items-center gap-1.5 text-textSecondary"><span className="h-2 w-2 rounded-sm bg-red-400/50"></span> Out</span>
      </div>
    </div>
  );
}

export default function Solutions() {
  return (
    <div className="relative overflow-hidden">
      {/* HERO */}
      <section className="relative">
        <div className="absolute inset-0 bg-grid opacity-30"></div>
        <div className="absolute top-0 right-1/4 h-96 w-96 rounded-full bg-accent/15 blur-3xl"></div>
        <div className="relative max-w-7xl mx-auto px-5 sm:px-8 pt-20 pb-14 md:pt-24 md:pb-16 text-center">
          <span className="text-xs font-bold tracking-widest text-accent uppercase">Solutions</span>
          <h1 className="mt-3 text-4xl md:text-6xl font-black tracking-tight text-white">
            Built for the workflows that{' '}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-accent to-accentWarm">move your industry</span>
          </h1>
          <p className="mt-5 max-w-2xl mx-auto text-lg text-textSecondary">
            From regulated healthcare data to real-time payments, Nexus ships pre-built playbooks and compliance guardrails for the industries with the highest stakes.
          </p>
        </div>
      </section>

      {/* INDUSTRIES */}
      <section className="max-w-7xl mx-auto px-5 sm:px-8 py-8 md:py-14 space-y-20 md:space-y-28">
        {SOLUTIONS.map((s, idx) => {
          const reverse = idx % 2 === 1;
          return (
            <article key={s.tag} className={`grid grid-cols-1 md:grid-cols-2 gap-10 lg:gap-16 items-center ${reverse ? 'md:[&>*:first-child]:order-2' : ''}`}>
              {/* Text */}
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface border border-borderc">
                  <span className={`h-2 w-2 rounded-full bg-gradient-to-r ${s.palette}`}></span>
                  <span className="text-xs font-bold tracking-widest text-textSecondary uppercase">{s.tag}</span>
                </div>
                <h2 className="mt-4 text-3xl md:text-4xl font-black text-white tracking-tight leading-tight">
                  {s.title}
                </h2>
                <p className="mt-4 text-textSecondary text-lg leading-relaxed">{s.desc}</p>
                <ul className="mt-6 space-y-3">
                  {s.bullets.map((b) => (
                    <li key={b} className="flex items-start gap-3 text-textPrimary">
                      <span className={`mt-1 h-5 w-5 grid place-items-center rounded-md bg-gradient-to-br ${s.palette} text-slate-900 text-xs font-bold shrink-0`}>✓</span>
                      <span>{b}</span>
                    </li>
                  ))}
                </ul>
                <div className="mt-8 flex items-center gap-6">
                  <div>
                    <div className={`text-3xl md:text-4xl font-black bg-clip-text text-transparent bg-gradient-to-r ${s.palette}`}>
                      {s.stat.v}
                    </div>
                    <div className="text-xs font-semibold tracking-widest text-textSecondary uppercase mt-1">{s.stat.k}</div>
                  </div>
                  <div className="h-12 w-px bg-borderc"></div>
                  <button className="text-sm font-semibold text-white hover:text-accent transition">
                    Read the case study →
                  </button>
                </div>
              </div>

              {/* Illustration */}
              <div className="relative">
                <div className={`absolute -inset-4 bg-gradient-to-br ${s.palette} opacity-20 blur-2xl`}></div>
                <div className="relative">
                  <Illustration kind={s.visual} palette={s.palette} />
                </div>
              </div>
            </article>
          );
        })}
      </section>

      {/* MORE INDUSTRIES */}
      <section className="max-w-7xl mx-auto px-5 sm:px-8 py-20">
        <div className="text-center mb-10">
          <h2 className="text-3xl md:text-4xl font-black text-white">And a lot more where that came from.</h2>
          <p className="mt-3 text-textSecondary">Purpose-built templates ready for your industry.</p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { t: 'SaaS & B2B', d: 'PLG signal orchestration' },
            { t: 'Logistics', d: 'Multi-carrier tracking' },
            { t: 'Manufacturing', d: 'IoT & MES sync' },
            { t: 'Media & Ads', d: 'Attribution pipelines' },
            { t: 'Education', d: 'SIS & LMS bridges' },
            { t: 'Real Estate', d: 'MLS enrichment' },
            { t: 'Insurance', d: 'Claims automation' },
            { t: 'Public Sector', d: 'FedRAMP-ready flows' },
          ].map((c) => (
            <div key={c.t} className="rounded-xl bg-surface/60 border border-borderc p-5 hover:border-accent transition group cursor-pointer">
              <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-accent/20 to-accentWarm/20 border border-accent/30 mb-3 group-hover:scale-110 transition-transform"></div>
              <div className="text-sm font-bold text-white">{c.t}</div>
              <div className="text-xs text-textSecondary mt-1">{c.d}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
