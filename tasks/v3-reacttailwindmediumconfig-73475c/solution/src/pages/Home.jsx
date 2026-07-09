import React from 'react';

const FEATURES = [
  {
    title: 'Unified API Layer',
    desc: 'One SDK, 400+ integrations. Ship connections in minutes, not months. Battle-tested at petabyte scale.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="h-6 w-6">
        <path d="M4 6h16M4 12h16M4 18h16" strokeLinecap="round" />
        <circle cx="7" cy="6" r="1.5" fill="currentColor" />
        <circle cx="14" cy="12" r="1.5" fill="currentColor" />
        <circle cx="17" cy="18" r="1.5" fill="currentColor" />
      </svg>
    ),
    stat: '400+ APIs',
  },
  {
    title: 'Real-Time Sync',
    desc: 'Bidirectional event streams under 50ms. Watch data flow live across every connected system on your grid.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="h-6 w-6">
        <path d="M4 12a8 8 0 0116 0M20 12a8 8 0 01-16 0" strokeLinecap="round" />
        <path d="M16 8l4-4M8 16l-4 4" strokeLinecap="round" />
      </svg>
    ),
    stat: '<50ms',
  },
  {
    title: 'Zero-Trust Security',
    desc: 'SOC 2 Type II, HIPAA, and ISO 27001 certified. End-to-end encryption with customer-managed keys.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="h-6 w-6">
        <path d="M12 3l8 3v6c0 5-3.5 8.5-8 9-4.5-.5-8-4-8-9V6l8-3z" strokeLinejoin="round" />
        <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    stat: 'SOC 2',
  },
  {
    title: 'Observability Suite',
    desc: 'Trace every request, monitor every workflow. AI-powered anomaly detection with self-healing retries.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="h-6 w-6">
        <path d="M3 3v18h18" strokeLinecap="round" />
        <path d="M7 15l4-6 3 4 4-8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    stat: '99.99%',
  },
];

const LOGOS = ['ATLASCORP', 'NORTHWIND', 'STELLAR', 'HELIX', 'VECTOR.io', 'ORBITAL', 'KINETIC', 'PRISM'];

export default function Home({ setActiveTab }) {
  return (
    <div className="relative overflow-hidden">
      {/* HERO */}
      <section className="relative">
        <div className="absolute inset-0 bg-grid opacity-40"></div>
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 h-[600px] w-[900px] rounded-full bg-accent/20 blur-[120px]"></div>
        <div className="absolute top-40 right-10 h-[400px] w-[400px] rounded-full bg-accentWarm/20 blur-[100px]"></div>

        <div className="relative max-w-7xl mx-auto px-5 sm:px-8 pt-20 pb-16 md:pt-28 md:pb-24">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-borderc bg-surface/60 backdrop-blur">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-xs font-medium text-textSecondary">
                <span className="text-white">Now shipping:</span> Nexus 4.0 with AI Workflow Studio
              </span>
              <span className="text-accent text-xs">→</span>
            </div>

            <h1 className="mt-6 text-5xl md:text-7xl font-black tracking-tight leading-[1.05]">
              <span className="text-white">Connect</span>{' '}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-accent via-cyan-300 to-accentWarm">
                Everything.
              </span>
              <br />
              <span className="text-textSecondary text-3xl md:text-5xl font-light">Automate anything.</span>
            </h1>

            <p className="mt-6 text-lg md:text-xl text-textSecondary max-w-2xl mx-auto leading-relaxed">
              Nexus is the integration platform for modern teams. Wire up your stack, orchestrate cross-app workflows, and ship revenue-critical automations — without owning infrastructure.
            </p>

            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={() => setActiveTab('page_pricing')}
                className="group px-6 py-3.5 rounded-xl font-semibold text-slate-900 bg-gradient-to-r from-accent to-accentWarm hover:brightness-110 shadow-lg shadow-accent/30 transition-all"
              >
                Start free 14-day trial
                <span className="ml-2 inline-block transition-transform group-hover:translate-x-1">→</span>
              </button>
              <button
                onClick={() => setActiveTab('page_docs')}
                className="px-6 py-3.5 rounded-xl font-semibold text-white bg-surface/60 border border-borderc hover:border-accent hover:bg-surface transition"
              >
                <span className="inline-block mr-2">▷</span> Watch product tour
              </button>
            </div>

            <div className="mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-textSecondary">
              <span className="flex items-center gap-1.5"><span className="text-accent">✓</span> No credit card required</span>
              <span className="flex items-center gap-1.5"><span className="text-accent">✓</span> Free forever plan</span>
              <span className="flex items-center gap-1.5"><span className="text-accent">✓</span> Cancel anytime</span>
            </div>
          </div>

          {/* APP MOCKUP */}
          <div className="relative mt-16 md:mt-20 mx-auto max-w-6xl">
            <div className="absolute -inset-4 bg-gradient-to-r from-accent/30 via-accentWarm/30 to-accent/30 blur-2xl opacity-60"></div>
            <div className="relative rounded-2xl border border-borderc bg-surface shadow-2xl shadow-accent/10 overflow-hidden">
              {/* Window chrome */}
              <div className="flex items-center gap-2 px-4 py-3 border-b border-borderc bg-background/60">
                <div className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded-full bg-red-400/70"></span>
                  <span className="h-3 w-3 rounded-full bg-yellow-400/70"></span>
                  <span className="h-3 w-3 rounded-full bg-emerald-400/70"></span>
                </div>
                <div className="flex-1 flex justify-center">
                  <div className="px-3 py-1 rounded-md bg-background/70 border border-borderc text-xs text-textSecondary font-mono">
                    app.nexus.io/workflows/customer-onboarding
                  </div>
                </div>
              </div>
              {/* App body */}
              <div className="grid grid-cols-12 min-h-[420px]">
                {/* Sidebar */}
                <aside className="col-span-3 border-r border-borderc bg-background/40 p-4">
                  <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase mb-3">Workflows</div>
                  <ul className="space-y-1.5">
                    {[
                      { name: 'Customer Onboarding', active: true },
                      { name: 'Lead Enrichment', active: false },
                      { name: 'Invoice Automation', active: false },
                      { name: 'Support Triage', active: false },
                      { name: 'Data Pipeline', active: false },
                    ].map((w) => (
                      <li key={w.name} className={`flex items-center gap-2 px-2.5 py-2 rounded-md text-xs ${w.active ? 'bg-accent/10 text-white' : 'text-textSecondary'}`}>
                        <span className={`h-1.5 w-1.5 rounded-full ${w.active ? 'bg-accent' : 'bg-borderc'}`}></span>
                        {w.name}
                      </li>
                    ))}
                  </ul>
                  <div className="mt-6 text-[10px] font-bold tracking-widest text-textSecondary uppercase mb-3">Integrations</div>
                  <div className="flex flex-wrap gap-1.5">
                    {['SF', 'HB', 'ST', 'SL', 'GH', 'AWS'].map((tag) => (
                      <span key={tag} className="h-7 w-7 rounded-md bg-surface border border-borderc grid place-items-center text-[10px] font-bold text-textSecondary">{tag}</span>
                    ))}
                  </div>
                </aside>
                {/* Canvas */}
                <div className="col-span-9 relative bg-grid p-6">
                  <div className="flex items-center justify-between mb-5">
                    <div>
                      <h3 className="text-sm font-semibold text-white">Customer Onboarding</h3>
                      <p className="text-[11px] text-textSecondary">Last run 2 min ago · 1,284 executions today</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-1 rounded-md text-[10px] font-semibold text-emerald-300 bg-emerald-500/10 border border-emerald-500/30">● LIVE</span>
                      <button className="px-3 py-1.5 rounded-md text-[11px] font-semibold text-slate-900 bg-accent">Run</button>
                    </div>
                  </div>

                  {/* Nodes */}
                  <div className="relative grid grid-cols-4 gap-4 items-center">
                    {[
                      { label: 'Trigger', sub: 'New Stripe customer', color: 'from-accent to-cyan-300' },
                      { label: 'Enrich', sub: 'Clearbit lookup', color: 'from-accentWarm to-fuchsia-400' },
                      { label: 'Notify', sub: 'Slack #sales', color: 'from-emerald-400 to-teal-300' },
                      { label: 'Create', sub: 'HubSpot deal', color: 'from-amber-400 to-orange-300' },
                    ].map((n, i) => (
                      <div key={n.label} className="relative">
                        <div className="rounded-xl bg-surface border border-borderc p-3 shadow-lg">
                          <div className={`h-8 w-8 rounded-lg bg-gradient-to-br ${n.color} grid place-items-center mb-2`}>
                            <span className="text-slate-900 text-xs font-bold">{n.label[0]}</span>
                          </div>
                          <div className="text-[11px] font-semibold text-white">{n.label}</div>
                          <div className="text-[10px] text-textSecondary">{n.sub}</div>
                        </div>
                        {i < 3 && (
                          <div className="hidden md:block absolute top-1/2 -right-3 -translate-y-1/2 text-accent text-lg">→</div>
                        )}
                      </div>
                    ))}
                  </div>

                  {/* Metric row */}
                  <div className="mt-6 grid grid-cols-3 gap-3">
                    {[
                      { k: 'Success rate', v: '99.94%' },
                      { k: 'Avg latency', v: '38ms' },
                      { k: 'Cost / run', v: '$0.0004' },
                    ].map((m) => (
                      <div key={m.k} className="rounded-lg bg-surface border border-borderc px-3 py-2">
                        <div className="text-[10px] text-textSecondary uppercase tracking-wider">{m.k}</div>
                        <div className="text-sm font-bold text-white">{m.v}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* LOGO STRIP */}
      <section className="border-y border-borderc/60 bg-surface/20">
        <div className="max-w-7xl mx-auto px-5 sm:px-8 py-10">
          <p className="text-center text-xs font-semibold tracking-widest text-textSecondary uppercase mb-6">
            Powering teams at 12,000+ companies
          </p>
          <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-4">
            {LOGOS.map((l) => (
              <span key={l} className="text-lg md:text-xl font-black tracking-tight text-textSecondary/70 hover:text-white transition">
                {l}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="max-w-7xl mx-auto px-5 sm:px-8 py-20 md:py-28">
        <div className="max-w-2xl">
          <span className="text-xs font-bold tracking-widest text-accent uppercase">Why Nexus</span>
          <h2 className="mt-3 text-4xl md:text-5xl font-black tracking-tight text-white">
            One platform. Every integration. Zero glue code.
          </h2>
          <p className="mt-4 text-lg text-textSecondary">
            Replace fragmented scripts and legacy iPaaS tools with an end-to-end system built for engineering velocity.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-5">
          {FEATURES.map((f) => (
            <div key={f.title} className="gradient-border p-6 md:p-8 group hover:shadow-xl hover:shadow-accent/10 transition">
              <div className="flex items-start justify-between mb-5">
                <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-accent/20 to-accentWarm/20 border border-accent/30 grid place-items-center text-accent group-hover:scale-110 transition-transform">
                  {f.icon}
                </div>
                <span className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-accent to-accentWarm">
                  {f.stat}
                </span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{f.title}</h3>
              <p className="text-textSecondary leading-relaxed">{f.desc}</p>
              <div className="mt-5 pt-5 border-t border-borderc/60 flex items-center text-sm font-medium text-accent">
                Learn more <span className="ml-1.5 transition-transform group-hover:translate-x-1">→</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* STATS */}
      <section className="max-w-7xl mx-auto px-5 sm:px-8 pb-20">
        <div className="rounded-3xl border border-borderc bg-gradient-to-br from-surface via-surface to-background p-8 md:p-14 relative overflow-hidden">
          <div className="absolute -top-20 -right-20 h-64 w-64 rounded-full bg-accent/20 blur-3xl"></div>
          <div className="absolute -bottom-20 -left-20 h-64 w-64 rounded-full bg-accentWarm/20 blur-3xl"></div>
          <div className="relative grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { k: 'Events per second', v: '4.2M' },
              { k: 'Uptime SLA', v: '99.99%' },
              { k: 'Countries served', v: '142' },
              { k: 'Enterprise customers', v: '2,800+' },
            ].map((s) => (
              <div key={s.k}>
                <div className="text-4xl md:text-5xl font-black bg-clip-text text-transparent bg-gradient-to-r from-accent to-accentWarm">
                  {s.v}
                </div>
                <div className="mt-2 text-xs font-semibold tracking-widest text-textSecondary uppercase">{s.k}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* TESTIMONIAL */}
      <section className="max-w-7xl mx-auto px-5 sm:px-8 pb-20 md:pb-28">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {[
            {
              quote: "Nexus replaced 4 different iPaaS vendors and cut our integration ops team's toil by 78%. The observability alone is worth the price.",
              name: 'Priya Ramanathan',
              role: 'VP Engineering, Helix Health',
            },
            {
              quote: "We wired Stripe, Salesforce, and our internal ledger together in an afternoon. What used to take a quarter now ships in a sprint.",
              name: 'Marcus Vogel',
              role: 'CTO, Orbital Finance',
            },
            {
              quote: "The AI Workflow Studio is a genuine step-change. Our analysts build automations that used to require a full engineer.",
              name: 'Kenji Watanabe',
              role: 'Head of RevOps, Stellar Retail',
            },
          ].map((t) => (
            <figure key={t.name} className="rounded-2xl bg-surface/60 border border-borderc p-6 md:p-7 backdrop-blur">
              <div className="flex gap-1 text-accent mb-4">{'★★★★★'.split('').map((s, i) => <span key={i}>{s}</span>)}</div>
              <blockquote className="text-textPrimary leading-relaxed">"{t.quote}"</blockquote>
              <figcaption className="mt-5 pt-5 border-t border-borderc/60 flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-accent to-accentWarm"></div>
                <div>
                  <div className="text-sm font-semibold text-white">{t.name}</div>
                  <div className="text-xs text-textSecondary">{t.role}</div>
                </div>
              </figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-7xl mx-auto px-5 sm:px-8 pb-24">
        <div className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-accent/20 via-surface to-accentWarm/20 border border-borderc p-10 md:p-16 text-center">
          <div className="absolute inset-0 bg-grid opacity-30"></div>
          <div className="relative">
            <h2 className="text-4xl md:text-5xl font-black text-white">Ready to connect your stack?</h2>
            <p className="mt-4 text-lg text-textSecondary max-w-xl mx-auto">
              Spin up your first workflow in under 3 minutes. No sales call required.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={() => setActiveTab('page_pricing')}
                className="px-7 py-3.5 rounded-xl font-semibold text-slate-900 bg-gradient-to-r from-accent to-accentWarm hover:brightness-110 shadow-lg shadow-accent/30 transition"
              >
                Start free trial
              </button>
              <button
                onClick={() => setActiveTab('page_contact')}
                className="px-7 py-3.5 rounded-xl font-semibold text-white border border-borderc bg-surface/50 hover:border-accent transition"
              >
                Talk to sales
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
