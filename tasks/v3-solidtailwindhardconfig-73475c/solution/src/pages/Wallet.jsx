import { For } from 'solid-js';

export default function Wallet() {
  const assets = [
    { symbol: 'BTC', name: 'Bitcoin', amount: 0.4128, value: 28242.90, alloc: 62.4, color: 'bg-amber-500', hex: '#f59e0b' },
    { symbol: 'ETH', name: 'Ethereum', amount: 2.844, value: 10940.10, alloc: 24.2, color: 'bg-indigo-500', hex: '#6366f1' },
    { symbol: 'SOL', name: 'Solana', amount: 24.1, value: 4396.80, alloc: 9.7, color: 'bg-purple-500', hex: '#a855f7' },
    { symbol: 'USDC', name: 'USD Coin', amount: 1204.20, value: 1204.20, alloc: 2.7, color: 'bg-blue-500', hex: '#3b82f6' },
    { symbol: 'ARB', name: 'Arbitrum', amount: 358.11, value: 426.80, alloc: 1.0, color: 'bg-sky-500', hex: '#0ea5e9' },
  ];

  const transactions = [
    { type: 'Buy', asset: 'BTC', amount: '+0.0244 BTC', value: '$1,668.42', time: '2 min ago', status: 'confirmed', hash: '0x4a9F...12b3' },
    { type: 'Swap', asset: 'ETH → USDC', amount: '−0.5 ETH', value: '$1,923.61', time: '1 hr ago', status: 'confirmed', hash: '0x88Ba...92aa' },
    { type: 'Stake', asset: 'USDC-USDT LP', amount: '+2,000 LP', value: '$2,000.00', time: '4 hrs ago', status: 'confirmed', hash: '0x1c22...aaf1' },
    { type: 'Receive', asset: 'SOL', amount: '+12.4 SOL', value: '$2,262.26', time: 'Yesterday', status: 'confirmed', hash: '0x9d41...b1c2' },
    { type: 'Reward', asset: 'CYPH', amount: '+42.8 CYPH', value: '$88.14', time: '2 days ago', status: 'confirmed', hash: '0x2f11...deb4' },
    { type: 'Sell', asset: 'AVAX', amount: '−22.4 AVAX', value: '$920.14', time: '3 days ago', status: 'confirmed', hash: '0x6a94...441c' },
    { type: 'Send', asset: 'USDT', amount: '−500 USDT', value: '$500.00', time: '5 days ago', status: 'confirmed', hash: '0x3e11...b8a2' },
  ];

  const typeStyle = (t) => {
    if (t === 'Buy' || t === 'Receive' || t === 'Stake' || t === 'Reward') return 'bg-accent/10 text-accent border-accent/30';
    if (t === 'Sell' || t === 'Send') return 'bg-danger/10 text-danger border-danger/30';
    return 'bg-accent-warm/10 text-accent-warm border-accent-warm/30';
  };

  // Build the donut chart using stroke-dasharray
  const CIRC = 2 * Math.PI * 60; // r = 60
  let cumulative = 0;
  const donutSegments = assets.map((a) => {
    const len = (a.alloc / 100) * CIRC;
    const offset = -cumulative;
    cumulative += len;
    return { len, offset, hex: a.hex };
  });

  return (
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <header class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
        <div>
          <span class="text-[11px] font-mono text-accent tracking-widest uppercase">// Wallet</span>
          <h1 class="mt-2 text-3xl md:text-4xl font-bold tracking-tight">Portfolio</h1>
          <div class="mt-2 flex items-center gap-2 text-[11px] font-mono text-text-secondary">
            <span class="w-1.5 h-1.5 rounded-full bg-accent pulse-dot"></span>
            <span>Connected · 0x4a9F...3bE1</span>
            <span class="ml-2 px-2 py-0.5 bg-surface border border-border rounded">Ethereum Mainnet</span>
          </div>
        </div>
        <div class="flex gap-2">
          <button class="px-4 py-2 text-xs font-semibold text-text-primary bg-surface border border-border hover:border-zinc-600 rounded-md">
            ↑ Send
          </button>
          <button class="px-4 py-2 text-xs font-semibold text-text-primary bg-surface border border-border hover:border-zinc-600 rounded-md">
            ↓ Receive
          </button>
          <button class="px-4 py-2 text-xs font-semibold text-background bg-accent hover:bg-emerald-400 rounded-md shadow-glow-accent">
            + Deposit
          </button>
        </div>
      </header>

      {/* Balance hero + allocation */}
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
        {/* Total balance card */}
        <div class="lg:col-span-2 relative bg-surface border border-border rounded-lg p-6 md:p-8 overflow-hidden">
          <div class="absolute -top-20 -right-20 w-64 h-64 bg-accent/10 rounded-full blur-3xl pointer-events-none"></div>
          <div class="absolute -bottom-20 -left-10 w-56 h-56 bg-accent-warm/5 rounded-full blur-3xl pointer-events-none"></div>
          <div class="relative">
            <div class="text-[10px] font-mono text-text-secondary uppercase tracking-wider">Total Balance</div>
            <div class="mt-2 flex items-baseline gap-3">
              <span class="text-5xl md:text-6xl font-bold font-mono text-text-primary tracking-tight">$45,210.80</span>
              <span class="text-sm font-mono font-semibold text-accent px-2 py-0.5 bg-accent/10 rounded">+$1,842.44</span>
            </div>
            <div class="mt-1 text-[11px] font-mono text-text-secondary">≈ 0.6608 BTC · Today +4.24%</div>

            <div class="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4 pt-6 border-t border-border">
              <div>
                <div class="text-[10px] font-mono text-text-secondary uppercase">Spot</div>
                <div class="text-lg font-mono font-semibold text-text-primary">$36,412.10</div>
              </div>
              <div>
                <div class="text-[10px] font-mono text-text-secondary uppercase">Staked</div>
                <div class="text-lg font-mono font-semibold text-text-primary">$6,842.44</div>
              </div>
              <div>
                <div class="text-[10px] font-mono text-text-secondary uppercase">Rewards Earned</div>
                <div class="text-lg font-mono font-semibold text-accent">$1,956.26</div>
              </div>
              <div>
                <div class="text-[10px] font-mono text-text-secondary uppercase">PnL (30d)</div>
                <div class="text-lg font-mono font-semibold text-accent">+18.4%</div>
              </div>
            </div>
          </div>
        </div>

        {/* Allocation donut */}
        <div class="bg-surface border border-border rounded-lg p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-[11px] font-semibold text-text-secondary uppercase tracking-widest">Asset Allocation</h3>
            <span class="text-[10px] font-mono text-accent">● live</span>
          </div>
          <div class="flex items-center gap-4">
            <div class="relative w-36 h-36 flex-shrink-0">
              <svg viewBox="0 0 160 160" class="w-full h-full -rotate-90">
                <circle cx="80" cy="80" r="60" fill="none" stroke="#27272a" stroke-width="18"/>
                <For each={donutSegments}>
                  {(seg) => (
                    <circle
                      cx="80"
                      cy="80"
                      r="60"
                      fill="none"
                      stroke={seg.hex}
                      stroke-width="18"
                      stroke-dasharray={`${seg.len} ${CIRC}`}
                      stroke-dashoffset={seg.offset}
                    />
                  )}
                </For>
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-[10px] font-mono text-text-secondary uppercase">Assets</span>
                <span class="text-2xl font-bold font-mono text-text-primary">{assets.length}</span>
              </div>
            </div>
            <div class="flex-1 space-y-1.5">
              <For each={assets}>
                {(a) => (
                  <div class="flex items-center justify-between text-[11px] font-mono">
                    <div class="flex items-center gap-2">
                      <span class={`w-2 h-2 rounded-sm ${a.color}`}></span>
                      <span class="text-text-primary">{a.symbol}</span>
                    </div>
                    <span class="text-text-secondary">{a.alloc.toFixed(1)}%</span>
                  </div>
                )}
              </For>
            </div>
          </div>
        </div>
      </div>

      {/* Holdings table */}
      <div class="bg-surface border border-border rounded-lg overflow-hidden mb-8">
        <div class="px-5 py-3 border-b border-border flex items-center justify-between">
          <h3 class="text-sm font-semibold text-text-primary">Your Holdings</h3>
          <span class="text-[10px] font-mono text-text-secondary">{assets.length} assets</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-border bg-background/40">
                <th class="text-left px-5 py-2 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Asset</th>
                <th class="text-right px-5 py-2 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Amount</th>
                <th class="text-right px-5 py-2 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Value</th>
                <th class="text-right px-5 py-2 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Allocation</th>
                <th class="text-right px-5 py-2 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody>
              <For each={assets}>
                {(a) => (
                  <tr class="border-b border-border/60 hover:bg-background/30">
                    <td class="px-5 py-3">
                      <div class="flex items-center gap-3">
                        <div class={`w-8 h-8 rounded-full ${a.color} flex items-center justify-center text-background text-[10px] font-bold`}>
                          {a.symbol.slice(0, 3)}
                        </div>
                        <div>
                          <div class="font-semibold text-text-primary">{a.name}</div>
                          <div class="text-[10px] font-mono text-text-secondary">{a.symbol}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-5 py-3 text-right font-mono text-text-primary">{a.amount.toLocaleString('en-US', { maximumFractionDigits: 4 })} {a.symbol}</td>
                    <td class="px-5 py-3 text-right font-mono text-text-primary">${a.value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                    <td class="px-5 py-3 text-right">
                      <div class="inline-flex items-center gap-2">
                        <div class="w-20 h-1.5 bg-background rounded-full overflow-hidden">
                          <div class={`h-full ${a.color}`} style={{ width: `${a.alloc}%` }}></div>
                        </div>
                        <span class="text-[11px] font-mono text-text-secondary w-12 text-right">{a.alloc.toFixed(1)}%</span>
                      </div>
                    </td>
                    <td class="px-5 py-3 text-right">
                      <button class="px-3 py-1 text-[11px] font-semibold text-accent bg-accent/10 hover:bg-accent hover:text-background border border-accent/30 rounded transition-all">
                        Trade
                      </button>
                    </td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </div>
      </div>

      {/* Transaction history */}
      <div class="bg-surface border border-border rounded-lg overflow-hidden">
        <div class="px-5 py-3 border-b border-border flex items-center justify-between">
          <h3 class="text-sm font-semibold text-text-primary">Recent Transactions</h3>
          <button class="text-[11px] font-mono text-accent hover:text-emerald-300">View all →</button>
        </div>
        <ul class="divide-y divide-border/60">
          <For each={transactions}>
            {(t) => (
              <li class="px-5 py-3 flex items-center gap-4 hover:bg-background/30">
                <span class={`px-2 py-0.5 text-[10px] font-mono font-semibold uppercase border rounded ${typeStyle(t.type)}`}>
                  {t.type}
                </span>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-semibold text-text-primary truncate">{t.asset}</div>
                  <div class="text-[10px] font-mono text-text-secondary">{t.hash} · {t.time}</div>
                </div>
                <div class="text-right">
                  <div class={`text-sm font-mono font-semibold ${t.amount.startsWith('+') ? 'text-accent' : t.amount.startsWith('-') || t.amount.startsWith('−') ? 'text-danger' : 'text-text-primary'}`}>
                    {t.amount}
                  </div>
                  <div class="text-[10px] font-mono text-text-secondary">{t.value}</div>
                </div>
                <div class="hidden md:flex items-center gap-1 text-[10px] font-mono text-accent">
                  <span class="w-1.5 h-1.5 rounded-full bg-accent"></span>
                  {t.status}
                </div>
              </li>
            )}
          </For>
        </ul>
      </div>
    </div>
  );
}
