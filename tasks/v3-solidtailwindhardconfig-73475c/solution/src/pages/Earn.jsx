import { createSignal, For } from 'solid-js';

export default function Earn() {
  const [tab, setTab] = createSignal('all');

  const pools = [
    { pair: 'USDC-USDT', apy: 12, tvl: '$418.4M', chain: 'Ethereum', risk: 'Low', color1: 'bg-blue-500', color2: 'bg-emerald-500', hot: false },
    { pair: 'ETH-USDT', apy: 18, tvl: '$284.1M', chain: 'Arbitrum', risk: 'Medium', color1: 'bg-indigo-500', color2: 'bg-emerald-500', hot: true },
    { pair: 'BTC-ETH', apy: 14, tvl: '$612.8M', chain: 'Ethereum', risk: 'Low', color1: 'bg-amber-500', color2: 'bg-indigo-500', hot: false },
    { pair: 'SOL-USDC', apy: 24, tvl: '$142.6M', chain: 'Solana', risk: 'High', color1: 'bg-purple-500', color2: 'bg-blue-500', hot: true },
    { pair: 'ARB-ETH', apy: 18, tvl: '$88.2M', chain: 'Arbitrum', risk: 'Medium', color1: 'bg-sky-500', color2: 'bg-indigo-500', hot: false },
    { pair: 'AVAX-USDC', apy: 24, tvl: '$54.9M', chain: 'Avalanche', risk: 'High', color1: 'bg-red-500', color2: 'bg-blue-500', hot: false },
  ];

  const riskColor = (r) =>
    r === 'Low' ? 'text-accent bg-accent/10 border-accent/30'
      : r === 'Medium' ? 'text-accent-warm bg-accent-warm/10 border-accent-warm/30'
      : 'text-danger bg-danger/10 border-danger/30';

  return (
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <header class="mb-10">
        <span class="text-[11px] font-mono text-accent tracking-widest uppercase">// Earn</span>
        <h1 class="mt-2 text-3xl md:text-4xl font-bold tracking-tight">Yield &amp; Staking Vaults</h1>
        <p class="mt-3 text-text-secondary max-w-2xl">
          Provide liquidity or stake single assets into audited vaults. Earn from trading fees, protocol emissions, and boosted incentives. Withdraw any time.
        </p>
      </header>

      {/* Stats bar */}
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
        <div class="bg-surface border border-border rounded-lg p-4">
          <div class="text-[10px] font-mono text-text-secondary uppercase tracking-wider">Total Value Locked</div>
          <div class="mt-1 text-2xl font-bold font-mono text-text-primary">$1.6B</div>
          <div class="text-[11px] font-mono text-accent">+4.2% this week</div>
        </div>
        <div class="bg-surface border border-border rounded-lg p-4">
          <div class="text-[10px] font-mono text-text-secondary uppercase tracking-wider">Average APY</div>
          <div class="mt-1 text-2xl font-bold font-mono text-accent">17.4%</div>
          <div class="text-[11px] font-mono text-text-secondary">Across 42 vaults</div>
        </div>
        <div class="bg-surface border border-border rounded-lg p-4">
          <div class="text-[10px] font-mono text-text-secondary uppercase tracking-wider">Rewards Paid (30d)</div>
          <div class="mt-1 text-2xl font-bold font-mono text-text-primary">$18.2M</div>
          <div class="text-[11px] font-mono text-text-secondary">In CYPH + fees</div>
        </div>
        <div class="bg-surface border border-border rounded-lg p-4">
          <div class="text-[10px] font-mono text-text-secondary uppercase tracking-wider">Active LPs</div>
          <div class="mt-1 text-2xl font-bold font-mono text-text-primary">14,822</div>
          <div class="text-[11px] font-mono text-accent">+284 today</div>
        </div>
      </div>

      {/* Tabs */}
      <div class="flex flex-wrap gap-2 mb-5">
        <For each={[
          { id: 'all', label: 'All Pools' },
          { id: 'stable', label: 'Stablecoins' },
          { id: 'volatile', label: 'Volatile' },
          { id: 'boosted', label: 'Boosted' },
        ]}>
          {(t) => (
            <button
              onClick={() => setTab(t.id)}
              class={`px-4 py-2 text-xs font-semibold rounded-md border transition-colors ${
                tab() === t.id
                  ? 'bg-accent/10 text-accent border-accent/40'
                  : 'bg-surface text-text-secondary border-border hover:text-text-primary'
              }`}
            >
              {t.label}
            </button>
          )}
        </For>
      </div>

      {/* Pool grid */}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <For each={pools}>
          {(p) => (
            <article class="bg-surface border border-border rounded-lg overflow-hidden hover:border-accent/50 hover:shadow-glow-accent transition-all">
              <div class="p-5">
                <div class="flex items-start justify-between mb-4">
                  <div class="flex items-center">
                    <div class="flex -space-x-2">
                      <div class={`w-9 h-9 rounded-full ${p.color1} ring-2 ring-surface flex items-center justify-center text-background text-[10px] font-bold`}>
                        {p.pair.split('-')[0].slice(0,3)}
                      </div>
                      <div class={`w-9 h-9 rounded-full ${p.color2} ring-2 ring-surface flex items-center justify-center text-background text-[10px] font-bold`}>
                        {p.pair.split('-')[1].slice(0,3)}
                      </div>
                    </div>
                    <div class="ml-3">
                      <div class="text-base font-bold text-text-primary">{p.pair}</div>
                      <div class="text-[10px] font-mono text-text-secondary uppercase">{p.chain}</div>
                    </div>
                  </div>
                  {p.hot && (
                    <span class="px-2 py-0.5 text-[10px] font-mono font-semibold text-accent-warm bg-accent-warm/10 border border-accent-warm/40 rounded shadow-glow-warm">
                      BOOSTED
                    </span>
                  )}
                </div>

                <div class="mb-4">
                  <div class="text-[10px] font-mono text-text-secondary uppercase tracking-wider">Annual Percentage Yield</div>
                  <div class="mt-1 flex items-baseline gap-2">
                    <span class="text-4xl font-bold font-mono bg-gradient-to-r from-accent to-emerald-300 bg-clip-text text-transparent">
                      {p.apy}%
                    </span>
                    <span class="text-xs font-mono text-text-secondary">APY</span>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-3 mb-5 pb-5 border-b border-border">
                  <div>
                    <div class="text-[10px] font-mono text-text-secondary uppercase">TVL</div>
                    <div class="text-sm font-mono text-text-primary">{p.tvl}</div>
                  </div>
                  <div>
                    <div class="text-[10px] font-mono text-text-secondary uppercase">Risk</div>
                    <span class={`inline-block mt-0.5 px-2 py-0.5 text-[10px] font-mono border rounded ${riskColor(p.risk)}`}>
                      {p.risk}
                    </span>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-2">
                  <button class="py-2.5 text-xs font-semibold text-background bg-accent hover:bg-emerald-400 rounded-md transition-all shadow-glow-accent">
                    Stake
                  </button>
                  <button class="py-2.5 text-xs font-semibold text-text-primary bg-background hover:bg-zinc-800 border border-border rounded-md transition-colors">
                    Unstake
                  </button>
                </div>
              </div>
            </article>
          )}
        </For>
      </div>

      {/* Info banner */}
      <div class="mt-10 bg-gradient-to-r from-accent/5 via-surface to-accent-warm/5 border border-border rounded-lg p-6 md:p-8 flex flex-col md:flex-row items-start md:items-center gap-6">
        <div class="w-14 h-14 rounded-lg bg-accent/10 border border-accent/30 flex items-center justify-center text-2xl">
          🔒
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-bold text-text-primary">Audited by Trail of Bits &amp; OpenZeppelin</h3>
          <p class="mt-1 text-sm text-text-secondary max-w-2xl">
            Every Cypher vault is protected by real-time risk monitoring and covered by a $50M protocol insurance fund. Withdrawals are always non-custodial.
          </p>
        </div>
        <button class="px-5 py-2.5 text-xs font-semibold text-accent bg-accent/10 hover:bg-accent/20 border border-accent/30 rounded-md whitespace-nowrap">
          View Audit Reports →
        </button>
      </div>
    </div>
  );
}
