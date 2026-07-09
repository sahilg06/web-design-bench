import React, { useState } from 'react';

const NAV = [
  {
    section: 'Getting Started',
    items: [
      { id: 'intro', label: 'Introduction' },
      { id: 'quickstart', label: 'Quickstart' },
      { id: 'concepts', label: 'Core concepts' },
      { id: 'auth', label: 'Authentication' },
    ],
  },
  {
    section: 'Workflows',
    items: [
      { id: 'triggers', label: 'Triggers' },
      { id: 'steps', label: 'Steps & actions' },
      { id: 'branching', label: 'Branching & loops' },
      { id: 'errors', label: 'Error handling' },
    ],
  },
  {
    section: 'API Reference',
    items: [
      { id: 'rest', label: 'REST API' },
      { id: 'sdks', label: 'SDKs' },
      { id: 'webhooks', label: 'Webhooks' },
      { id: 'events', label: 'Event schema' },
    ],
  },
  {
    section: 'Deploy',
    items: [
      { id: 'cli', label: 'CLI' },
      { id: 'cicd', label: 'CI/CD' },
      { id: 'terraform', label: 'Terraform' },
    ],
  },
];

function CodeBlock({ lang, code, filename }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(code);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };
  return (
    <div className="rounded-xl overflow-hidden border border-borderc bg-background/70 my-5">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-borderc bg-surface/60">
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-accent/70"></span>
          <span className="text-[11px] font-mono text-textSecondary">{filename}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-[10px] font-bold tracking-widest text-textSecondary uppercase">{lang}</span>
          <button onClick={copy} className="text-[11px] font-medium text-accent hover:text-white transition">
            {copied ? 'Copied ✓' : 'Copy'}
          </button>
        </div>
      </div>
      <pre className="p-4 text-[13px] leading-relaxed overflow-x-auto font-mono text-textPrimary">
        <code>{code}</code>
      </pre>
    </div>
  );
}

export default function Docs() {
  const [active, setActive] = useState('quickstart');

  return (
    <div className="max-w-7xl mx-auto px-5 sm:px-8 py-10 md:py-14">
      <div className="grid grid-cols-1 lg:grid-cols-[240px_1fr] xl:grid-cols-[240px_1fr_220px] gap-10">
        {/* SIDEBAR */}
        <aside className="lg:sticky lg:top-24 lg:self-start">
          <div className="mb-6">
            <div className="relative">
              <input
                type="text"
                placeholder="Search docs…"
                className="w-full pl-9 pr-14 py-2.5 rounded-lg bg-surface border border-borderc text-sm text-white placeholder:text-textSecondary focus:border-accent focus:outline-none"
              />
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="absolute left-3 top-3 h-4 w-4 text-textSecondary">
                <circle cx="11" cy="11" r="7" /><path d="M20 20l-3.5-3.5" strokeLinecap="round" />
              </svg>
              <span className="absolute right-3 top-2.5 text-[10px] font-mono px-1.5 py-0.5 rounded bg-background border border-borderc text-textSecondary">⌘K</span>
            </div>
          </div>
          <nav className="space-y-6">
            {NAV.map((sec) => (
              <div key={sec.section}>
                <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase mb-2 px-2">{sec.section}</div>
                <ul className="space-y-0.5">
                  {sec.items.map((i) => {
                    const isActive = active === i.id;
                    return (
                      <li key={i.id}>
                        <button
                          onClick={() => setActive(i.id)}
                          className={`w-full text-left px-3 py-1.5 rounded-md text-sm transition ${
                            isActive
                              ? 'text-white bg-accent/10 border-l-2 border-accent'
                              : 'text-textSecondary hover:text-white hover:bg-surface/60'
                          }`}
                        >
                          {i.label}
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </nav>
        </aside>

        {/* CONTENT */}
        <article className="min-w-0">
          <div className="flex items-center gap-2 text-xs text-textSecondary mb-4">
            <span>Docs</span>
            <span>/</span>
            <span>Getting Started</span>
            <span>/</span>
            <span className="text-white">Quickstart</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-black text-white tracking-tight">
            Quickstart
          </h1>
          <p className="mt-3 text-lg text-textSecondary">
            Build and ship your first Nexus workflow in under 3 minutes. This guide walks through installation, authentication, and running your first automated event.
          </p>

          <div className="mt-6 flex flex-wrap items-center gap-4 text-xs">
            <span className="flex items-center gap-2 text-textSecondary">
              <span className="h-6 w-6 rounded-full bg-gradient-to-br from-accent to-accentWarm"></span>
              Written by Ellis Marchetti · Updated Jun 24, 2026
            </span>
            <span className="px-2 py-1 rounded-md bg-accent/10 border border-accent/30 text-accent font-semibold">v4.0</span>
          </div>

          {/* Callout */}
          <div className="mt-8 rounded-xl border border-accent/40 bg-accent/5 p-4 flex items-start gap-3">
            <span className="mt-0.5 h-6 w-6 rounded-md bg-accent/20 text-accent grid place-items-center shrink-0">i</span>
            <div className="text-sm text-textPrimary">
              <strong className="text-white">Heads up:</strong> You'll need a free Nexus account and Node.js 18+. Grab your API key from{' '}
              <span className="font-mono text-accent">Settings → API</span>.
            </div>
          </div>

          <h2 id="install" className="mt-10 text-2xl font-bold text-white">1. Install the CLI</h2>
          <p className="mt-2 text-textSecondary leading-relaxed">
            The Nexus CLI is the fastest way to scaffold, test, and deploy workflows locally.
          </p>
          <CodeBlock
            lang="bash"
            filename="terminal"
            code={`# npm
npm install -g @nexus/cli

# or with pnpm
pnpm add -g @nexus/cli

# verify installation
nexus --version
# → nexus v4.0.2`}
          />

          <h2 className="mt-10 text-2xl font-bold text-white">2. Authenticate</h2>
          <p className="mt-2 text-textSecondary leading-relaxed">
            Log in once and every subsequent CLI command inherits your credentials via secure keychain storage.
          </p>
          <CodeBlock
            lang="bash"
            filename="terminal"
            code={`nexus login
# Opens https://app.nexus.io/cli/auth in your browser
# ✓ Authenticated as ellis@atlascorp.com
# ✓ Workspace: atlascorp-prod`}
          />

          <h2 className="mt-10 text-2xl font-bold text-white">3. Define your first workflow</h2>
          <p className="mt-2 text-textSecondary leading-relaxed">
            Workflows are declared as plain JavaScript modules. Every workflow exports a <span className="font-mono text-accent">trigger</span> and one or more <span className="font-mono text-accent">steps</span>.
          </p>
          <CodeBlock
            lang="javascript"
            filename="workflows/welcome-email.js"
            code={`import { defineWorkflow, stripe, sendgrid } from '@nexus/sdk';

export default defineWorkflow({
  name: 'welcome-email',
  trigger: stripe.event('customer.created'),

  steps: async ({ event, ctx }) => {
    const { email, name } = event.data.object;

    ctx.log.info(\`New customer: \${email}\`);

    await sendgrid.send({
      to: email,
      template: 'welcome-v2',
      data: { firstName: name.split(' ')[0] },
    });

    return { status: 'sent', email };
  },
});`}
          />

          <h2 className="mt-10 text-2xl font-bold text-white">4. Deploy</h2>
          <p className="mt-2 text-textSecondary leading-relaxed">
            One command pushes your workflow to Nexus's global execution grid.
          </p>
          <CodeBlock
            lang="bash"
            filename="terminal"
            code={`nexus deploy workflows/welcome-email.js

✓ Bundled workflow (23 KB)
✓ Uploaded to nexus.io
✓ Trigger registered: stripe.customer.created
✓ Live at https://app.nexus.io/w/welcome-email

⚡ Ready to receive events`}
          />

          <div className="mt-10 rounded-xl border border-borderc bg-surface/60 p-6">
            <h3 className="text-lg font-bold text-white">What's next?</h3>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
              {[
                { t: 'Connect more services', d: 'Browse 400+ integrations.' },
                { t: 'Learn about branching', d: 'Conditional and parallel steps.' },
                { t: 'Set up alerts', d: 'Route failures to Slack or PagerDuty.' },
                { t: 'Ship to production', d: 'CI/CD with GitHub Actions.' },
              ].map((x) => (
                <a key={x.t} href="#" className="rounded-lg border border-borderc bg-background/60 p-4 hover:border-accent transition group">
                  <div className="text-sm font-semibold text-white">{x.t} <span className="text-accent group-hover:translate-x-1 inline-block transition-transform">→</span></div>
                  <div className="text-xs text-textSecondary mt-1">{x.d}</div>
                </a>
              ))}
            </div>
          </div>

          <div className="mt-10 pt-6 border-t border-borderc flex items-center justify-between">
            <button className="text-sm text-textSecondary hover:text-white transition">← Introduction</button>
            <button className="text-sm text-accent hover:text-white transition">Core concepts →</button>
          </div>
        </article>

        {/* ON-PAGE NAV */}
        <aside className="hidden xl:block sticky top-24 self-start">
          <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase mb-3">On this page</div>
          <ul className="space-y-1.5 border-l border-borderc">
            {[
              { l: 'Install the CLI', a: true },
              { l: 'Authenticate' },
              { l: 'Define your workflow' },
              { l: 'Deploy' },
              { l: 'What\'s next?' },
            ].map((i) => (
              <li key={i.l}>
                <a href="#" className={`block pl-3 text-sm py-1 border-l-2 -ml-px ${i.a ? 'border-accent text-white' : 'border-transparent text-textSecondary hover:text-white'}`}>
                  {i.l}
                </a>
              </li>
            ))}
          </ul>

          <div className="mt-8 rounded-xl border border-borderc bg-surface/40 p-4">
            <div className="text-xs font-bold text-white">Was this helpful?</div>
            <div className="mt-3 flex gap-2">
              <button className="flex-1 py-1.5 rounded-md text-xs bg-background border border-borderc text-textSecondary hover:text-white hover:border-accent transition">👍 Yes</button>
              <button className="flex-1 py-1.5 rounded-md text-xs bg-background border border-borderc text-textSecondary hover:text-white hover:border-accent transition">👎 No</button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
