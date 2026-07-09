import { For } from 'solid-js';

export default function Home(props) {
  const ticker = [
    { s: 'BTC', p: '68,412.90', c: '+2.14%', up: true },
    { s: 'ETH', p: '3,847.22', c: '+1.82%', up: true },
    { s: 'SOL', p: '182.44', c: '+5.31%', up: true },
    { s: 'AVAX', p: '41.08', c: '-0.72%', up: false },
    { s: 'ARB', p: '1.184', c: '+3.05%', up: true },
    { s: 'OP', p: '2.417', c: '-1.44%', up: false },
    { s: 'LINK', p: '18.92', c: '+0.94%', up: true },
    { s: 'MATIC', p: '0.7241', c: '-2.11%', up: false },
    { s: 'DOGE', p: '0.1583', c: '+4.62%', up: true },
    { s: 'ATOM', p: '9.812', c: '+1.28%', up: true },
    { s: 'DOT', p: '7.104', c: '-0.55%', up: false },
    { s: 'ADA', p: '0.4712', c: '+2.87%', up: true },
  ];

  const markets = [
    { symbol: 'BTC', name: 'Bitcoin', price: '68,412.90', change: '+2.14%', up: true, volume: '$28.4B', color: 'bg-amber-500' },
    { symbol: 'ETH', name: 'Ethereum', price: '3,847.22', change: '+1.82%', up: true, volume: '$14.7B', color: 'bg-indigo-500' },
    { symbol: 'SOL', name: 'Solana', price: '182.44', change: '+5.31%', up: true, volume: '$6.2B', color: 'bg-purple-500' },
    { symbol: 'AVAX', name: 'Avalanche', price: '41.08', change: '-0.72%', up: false, volume: '$1.9B', color: 'bg-red-500' },
  ];

  const features = [
    { icon: '⚡', title: 'Sub-100ms Execution', body: 'Order matching backed by a custom rollup that clears trades faster than any centralized venue.' },
    { icon: '🛡️', title: 'Non-Custodial', body: 'Your keys, your coins. Cypher never touches user funds — every trade settles on-chain atomically.' },
    { icon: '🔗', title: '14 Chains, One Book', body: 'Unified liquidity across Ethereum, Solana, Base, Arbitrum, and eleven other networks.' },
    { icon: '💧', title: 'Deep Liquidity', body: '$4.8B in cumulative TVL delivers razor-thin spreads on over 1,200 trading pairs.' },
  ];

  return (
    <div>
      {/* Ticker */}
      <div class="border-b border-border bg-surface/40 overflow-hidden">
        <div class="flex ticker-track whitespace-nowrap py-2.5">
          <For each={[...ticker, ...ticker]}>
            {(t) => (
              <div class="inline-flex items-center gap-3 px-6 border-r border-border/60">
                <span class="text-[11px] font-mono text-text-secondary tracking-wider">{t.s}/USDT</span>
                <span class="text-[13px] font-mono font-medium text-text-primary">${t.p}</span>
                <span class={`text-[11px] font-mono font-semibold ${t.up ? 'text-accent' : 'text-danger'}`}>
                  {t.c}
                </span>
              </div>
            )}
          </For>
        </div>
      </div>

      {/* Hero */}
      <section class="relative overflow-hidden">
        <div class="absolute inset-0 grid-bg opacity-60 pointer-events-none"></div>
        <div class="absolute top-20 -left-20 w-96 h-96 bg-accent/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute top-40 right-10 w-80 h-80 bg-accent-warm/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <div class="grid lg:grid-cols-12 gap-10 items-center">
            <div class="lg:col-span-7">
              <div class="inline-flex items-center gap-2 px-3 py-1.5 border border-accent/30 bg-accent/5 rounded-full mb-6">
                <span class="w-1.5 h-1.5 rounded-full bg-accent pulse-dot"></span>
                <span class="text-[11px] font-mono text-accent tracking-widest uppercase">Cypher v4.2 Live on Mainnet</span>
              </div>
              <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.02]">
                Trade at
                <br />
                <span class="bg-gradient-to-r from-accent via-emerald-400 to-accent-warm bg-clip-text text-transparent">
                  Light Speed.
                </span>
              </h1>
              <p class="mt-6 text-lg text-text-secondary max-w-xl leading-relaxed">
                Cypher is a next-generation decentralized exchange for professionals — deep order books, cross-chain liquidity, and settlement in under 100 milliseconds. Custody stays yours.
              </p>
              <div class="mt-8 flex flex-col sm:flex-row gap-3">
                <button
                  onClick={() => props.onNavigate('page_trade')}
                  class="px-6 py-3 text-sm font-semibold text-background bg-accent hover:bg-emerald-400 rounded-md transition-all shadow-glow-accent"
                >
                  Launch Terminal →
                </button>
                <button
                  onClick={() => props.onNavigate('page_markets')}
                  class="px-6 py-3 text-sm font-semibold text-text-primary bg-surface hover:bg-zinc-800 border border-border rounded-md transition-colors"
                >
                  Explore Markets
                </button>
              </div>

              <div class="mt-10 grid grid-cols-3 gap-6 max-w-lg">
                <div>
                  <div class="text-2xl font-bold font-mono text-text-primary">$4.8B</div>
                  <div class="text-[11px] font-mono text-text-secondary uppercase tracking-wider mt-1">Total TVL</div>
                </div>
                <div class="border-l border-border pl-6">
                  <div class="text-2xl font-bold font-mono text-text-primary">1,204</div>
                  <div class="text-[11px] font-mono text-text-secondary uppercase tracking-wider mt-1">Markets</div>
                </div>
                <div class="border-l border-border pl-6">
                  <div class="text-2xl font-bold font-mono text-accent">98ms</div>
                  <div class="text-[11px] font-mono text-text-secondary uppercase tracking-wider mt-1">Avg. Fill</div>
                </div>
              </div>
            </div>

            {/* Mock trading panel */}
            <div class="lg:col-span-5">
              <div class="relative bg-surface border border-border rounded-lg overflow-hidden shadow-2xl">
                <div class="flex items-center justify-between px-4 py-3 border-b border-border bg-background/60">
                  <div class="flex items-center gap-3">
                    <div class="flex gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-full bg-danger/70"></span>
                      <span class="w-2.5 h-2.5 rounded-full bg-accent-warm/70"></span>
                      <span class="w-2.5 h-2.5 rounded-full bg-accent/70"></span>
                    </div>
                    <span class="text-[11px] font-mono text-text-secondary">terminal — btc-usdt</span>
                  </div>
                  <span class="text-[10px] font-mono text-accent">● LIVE</span>
                </div>
                <div class="p-4 space-y-2 font-mono text-[12px]">
                  <div class="flex items-baseline justify-between">
                    <span class="text-text-secondary">BTC/USDT</span>
                    <span class="text-text-primary text-2xl font-bold">$68,412.90</span>
                  </div>
                  <div class="flex items-center gap-2 text-[11px]">
                    <span class="px-1.5 py-0.5 rounded bg-accent/15 text-accent">+2.14%</span>
                    <span class="text-text-secondary">24h</span>
                  </div>

                  <div class="mt-4 h-32 relative bg-background/40 rounded border border-border overflow-hidden">
                    <svg viewBox="0 0 300 100" class="w-full h-full">
                      <defs>
                        <linearGradient id="chartFill" x1="0" x2="0" y1="0" y2="1">
                          <stop offset="0%" stop-color="#10b981" stop-opacity="0.35" />
                          <stop offset="100%" stop-color="#10b981" stop-opacity="0" />
                        </linearGradient>
                      </defs>
                      <path d="M0,70 L20,65 L40,72 L60,55 L80,60 L100,42 L120,48 L140,38 L160,44 L180,30 L200,35 L220,22 L240,28 L260,18 L280,24 L300,12 L300,100 L0,100 Z" fill="url(#chartFill)"/>
                      <path d="M0,70 L20,65 L40,72 L60,55 L80,60 L100,42 L120,48 L140,38 L160,44 L180,30 L200,35 L220,22 L240,28 L260,18 L280,24 L300,12" fill="none" stroke="#10b981" stroke-width="1.5"/>
                    </svg>
                  </div>

                  <div class="grid grid-cols-2 gap-2 mt-3">
                    <button class="py-2 text-[11px] font-semibold text-accent bg-accent/10 hover:bg-accent/20 border border-accent/30 rounded">
                      BUY 0.05 BTC
                    </button>
                    <button class="py-2 text-[11px] font-semibold text-danger bg-danger/10 hover:bg-danger/20 border border-danger/30 rounded">
                      SELL 0.05 BTC
                    </button>
                  </div>
                  <div class="pt-3 border-t border-border/60 grid grid-cols-3 gap-2 text-[10px]">
                    <div>
                      <div class="text-text-secondary">Bid</div>
                      <div class="text-accent">68,411.20</div>
                    </div>
                    <div>
                      <div class="text-text-secondary">Ask</div>
                      <div class="text-danger">68,414.60</div>
                    </div>
                    <div>
                      <div class="text-text-secondary">Spread</div>
                      <div class="text-text-primary">0.005%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Market summary cards */}
      <section class="border-t border-border bg-surface/20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div class="flex items-end justify-between mb-8">
            <div>
              <span class="text-[11px] font-mono text-accent tracking-widest uppercase">// Live Markets</span>
              <h2 class="mt-2 text-3xl md:text-4xl font-bold tracking-tight">Top Movers, Right Now</h2>
            </div>
            <button
              onClick={() => props.onNavigate('page_markets')}
              class="hidden sm:inline text-sm text-accent hover:text-emerald-300 font-medium"
            >
              View all markets →
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <For each={markets}>
              {(m) => (
                <article class="group bg-surface border border-border rounded-lg p-5 hover:border-accent/50 hover:shadow-glow-accent transition-all cursor-pointer">
                  <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center gap-3">
                      <div class={`w-9 h-9 rounded-full ${m.color} flex items-center justify-center text-background text-[11px] font-bold`}>
                        {m.symbol}
                      </div>
                      <div>
                        <div class="text-sm font-semibold text-text-primary">{m.name}</div>
                        <div class="text-[10px] font-mono text-text-secondary">{m.symbol}/USDT</div>
                      </div>
                    </div>
                    <span class={`text-[11px] font-mono font-semibold px-2 py-0.5 rounded ${m.up ? 'bg-accent/15 text-accent' : 'bg-danger/15 text-danger'}`}>
                      {m.change}
                    </span>
                  </div>
                  <div class="text-2xl font-bold font-mono text-text-primary">${m.price}</div>
                  <div class="mt-1 text-[11px] font-mono text-text-secondary">Vol {m.volume}</div>
                  <div class="mt-4 h-10 relative">
                    <svg viewBox="0 0 200 40" class="w-full h-full">
                      <path
                        d={m.up
                          ? "M0,32 L20,28 L40,30 L60,22 L80,24 L100,18 L120,14 L140,20 L160,10 L180,12 L200,4"
                          : "M0,10 L20,14 L40,12 L60,20 L80,18 L100,26 L120,24 L140,20 L160,30 L180,28 L200,34"}
                        fill="none"
                        stroke={m.up ? '#10b981' : '#ef4444'}
                        stroke-width="1.5"
                      />
                    </svg>
                  </div>
                </article>
              )}
            </For>
          </div>
        </div>
      </section>

      {/* Features */}
      <section class="border-t border-border">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div class="max-w-2xl mb-12">
            <span class="text-[11px] font-mono text-accent tracking-widest uppercase">// Infrastructure</span>
            <h2 class="mt-2 text-3xl md:text-4xl font-bold tracking-tight">Engineered for the professional trader.</h2>
            <p class="mt-4 text-text-secondary leading-relaxed">
              Cypher runs on a purpose-built execution rollup with a decentralized sequencer set and cryptographic proofs of every fill.
            </p>
          </div>
          <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <For each={features}>
              {(f) => (
                <div class="bg-surface border border-border rounded-lg p-6 hover:border-accent/40 transition-colors">
                  <div class="w-10 h-10 rounded-md bg-accent/10 border border-accent/30 flex items-center justify-center text-lg mb-4">
                    {f.icon}
                  </div>
                  <h3 class="text-base font-semibold text-text-primary mb-2">{f.title}</h3>
                  <p class="text-sm text-text-secondary leading-relaxed">{f.body}</p>
                </div>
              )}
            </For>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section class="border-t border-border bg-gradient-to-br from-surface via-background to-surface">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <h2 class="text-3xl md:text-5xl font-bold tracking-tight">Ready to trade?</h2>
          <p class="mt-4 text-text-secondary max-w-xl mx-auto">
            No sign-ups, no KYC, no waiting. Connect a wallet and place your first order in under 30 seconds.
          </p>
          <div class="mt-8 flex flex-col sm:flex-row justify-center gap-3">
            <button
              onClick={() => props.onNavigate('page_trade')}
              class="px-8 py-3 text-sm font-semibold text-background bg-accent hover:bg-emerald-400 rounded-md shadow-glow-accent transition-all"
            >
              Open Trading Terminal
            </button>
            <button
              onClick={() => props.onNavigate('page_earn')}
              class="px-8 py-3 text-sm font-semibold text-accent-warm bg-accent-warm/5 hover:bg-accent-warm/10 border border-accent-warm/40 rounded-md transition-colors"
            >
              Earn up to 24% APY
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
