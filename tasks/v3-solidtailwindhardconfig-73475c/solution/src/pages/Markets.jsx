import { createSignal, createMemo, For } from 'solid-js';

export default function Markets(props) {
  const [filter, setFilter] = createSignal('all');
  const [search, setSearch] = createSignal('');

  const rows = [
    { rank: 1, symbol: 'BTC', name: 'Bitcoin', price: 68412.90, change: 2.14, volume: '28.4B', mcap: '1.34T', cat: 'layer1', color: 'bg-amber-500' },
    { rank: 2, symbol: 'ETH', name: 'Ethereum', price: 3847.22, change: 1.82, volume: '14.7B', mcap: '462.1B', cat: 'layer1', color: 'bg-indigo-500' },
    { rank: 3, symbol: 'SOL', name: 'Solana', price: 182.44, change: 5.31, volume: '6.2B', mcap: '84.3B', cat: 'layer1', color: 'bg-purple-500' },
    { rank: 4, symbol: 'AVAX', name: 'Avalanche', price: 41.08, change: -0.72, volume: '1.9B', mcap: '16.2B', cat: 'layer1', color: 'bg-red-500' },
    { rank: 5, symbol: 'ARB', name: 'Arbitrum', price: 1.184, change: 3.05, volume: '842M', mcap: '3.9B', cat: 'layer2', color: 'bg-sky-500' },
    { rank: 6, symbol: 'OP', name: 'Optimism', price: 2.417, change: -1.44, volume: '412M', mcap: '2.7B', cat: 'layer2', color: 'bg-rose-500' },
    { rank: 7, symbol: 'MATIC', name: 'Polygon', price: 0.7241, change: -2.11, volume: '618M', mcap: '7.1B', cat: 'layer2', color: 'bg-violet-500' },
    { rank: 8, symbol: 'LINK', name: 'Chainlink', price: 18.92, change: 0.94, volume: '512M', mcap: '11.8B', cat: 'defi', color: 'bg-blue-500' },
    { rank: 9, symbol: 'UNI', name: 'Uniswap', price: 9.842, change: 2.61, volume: '204M', mcap: '5.9B', cat: 'defi', color: 'bg-pink-500' },
    { rank: 10, symbol: 'AAVE', name: 'Aave', price: 112.44, change: 4.28, volume: '186M', mcap: '1.6B', cat: 'defi', color: 'bg-fuchsia-500' },
    { rank: 11, symbol: 'MKR', name: 'Maker', price: 2418.10, change: -0.42, volume: '78M', mcap: '2.2B', cat: 'defi', color: 'bg-teal-500' },
    { rank: 12, symbol: 'DOGE', name: 'Dogecoin', price: 0.1583, change: 4.62, volume: '1.4B', mcap: '22.4B', cat: 'meme', color: 'bg-yellow-500' },
    { rank: 13, symbol: 'SHIB', name: 'Shiba Inu', price: 0.0000241, change: 7.18, volume: '822M', mcap: '14.2B', cat: 'meme', color: 'bg-orange-500' },
    { rank: 14, symbol: 'PEPE', name: 'Pepe', price: 0.0000112, change: 12.44, volume: '648M', mcap: '4.8B', cat: 'meme', color: 'bg-lime-500' },
    { rank: 15, symbol: 'ATOM', name: 'Cosmos', price: 9.812, change: 1.28, volume: '164M', mcap: '3.8B', cat: 'layer1', color: 'bg-cyan-500' },
  ];

  const filters = [
    { id: 'all', label: 'All Markets' },
    { id: 'layer1', label: 'Layer 1' },
    { id: 'layer2', label: 'Layer 2' },
    { id: 'defi', label: 'DeFi' },
    { id: 'meme', label: 'Memes' },
  ];

  const filtered = createMemo(() => {
    const q = search().toLowerCase();
    return rows.filter((r) => {
      const catMatch = filter() === 'all' || r.cat === filter();
      const qMatch = !q || r.symbol.toLowerCase().includes(q) || r.name.toLowerCase().includes(q);
      return catMatch && qMatch;
    });
  });

  const fmtPrice = (p) => p < 0.01 ? p.toFixed(7) : p < 1 ? p.toFixed(4) : p.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  return (
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <header class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
        <div>
          <span class="text-[11px] font-mono text-accent tracking-widest uppercase">// Markets</span>
          <h1 class="mt-2 text-3xl md:text-4xl font-bold tracking-tight">All Markets</h1>
          <p class="mt-2 text-sm text-text-secondary">1,204 spot pairs · Data streamed via Cypher aggregator</p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="bg-surface border border-border rounded-md px-3 py-2">
            <div class="text-[10px] font-mono text-text-secondary uppercase">Total Volume</div>
            <div class="text-sm font-mono font-semibold text-text-primary">$54.2B</div>
          </div>
          <div class="bg-surface border border-border rounded-md px-3 py-2">
            <div class="text-[10px] font-mono text-text-secondary uppercase">Pairs</div>
            <div class="text-sm font-mono font-semibold text-text-primary">1,204</div>
          </div>
          <div class="bg-surface border border-border rounded-md px-3 py-2">
            <div class="text-[10px] font-mono text-text-secondary uppercase">Gainers</div>
            <div class="text-sm font-mono font-semibold text-accent">742</div>
          </div>
          <div class="bg-surface border border-border rounded-md px-3 py-2">
            <div class="text-[10px] font-mono text-text-secondary uppercase">Losers</div>
            <div class="text-sm font-mono font-semibold text-danger">462</div>
          </div>
        </div>
      </header>

      <div class="flex flex-col md:flex-row md:items-center gap-3 mb-4">
        <div class="flex overflow-x-auto -mx-1 md:mx-0">
          <For each={filters}>
            {(f) => (
              <button
                onClick={() => setFilter(f.id)}
                class={`px-4 py-2 mx-1 text-xs font-semibold rounded-md whitespace-nowrap transition-colors border ${
                  filter() === f.id
                    ? 'bg-accent/10 text-accent border-accent/40'
                    : 'bg-surface text-text-secondary border-border hover:text-text-primary'
                }`}
              >
                {f.label}
              </button>
            )}
          </For>
        </div>
        <div class="flex-1 md:max-w-xs md:ml-auto">
          <div class="relative">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="7" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
            <input
              type="text"
              value={search()}
              onInput={(e) => setSearch(e.currentTarget.value)}
              placeholder="Search assets..."
              class="w-full pl-9 pr-3 py-2 text-sm bg-surface border border-border rounded-md text-text-primary placeholder:text-text-secondary focus:outline-none focus:border-accent/60"
            />
          </div>
        </div>
      </div>

      <div class="bg-surface border border-border rounded-lg overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-border bg-background/40">
                <th class="text-left px-4 py-3 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">#</th>
                <th class="text-left px-4 py-3 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Asset</th>
                <th class="text-right px-4 py-3 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Price</th>
                <th class="text-right px-4 py-3 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">24h Change</th>
                <th class="text-right px-4 py-3 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider hidden md:table-cell">Volume 24h</th>
                <th class="text-right px-4 py-3 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider hidden lg:table-cell">Market Cap</th>
                <th class="text-right px-4 py-3 text-[10px] font-mono font-semibold text-text-secondary uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody>
              <For each={filtered()}>
                {(r) => (
                  <tr class="border-b border-border/60 hover:bg-background/40 transition-colors">
                    <td class="px-4 py-3 text-[12px] font-mono text-text-secondary">{r.rank}</td>
                    <td class="px-4 py-3">
                      <div class="flex items-center gap-3">
                        <div class={`w-8 h-8 rounded-full ${r.color} flex items-center justify-center text-background text-[10px] font-bold`}>
                          {r.symbol.slice(0, 3)}
                        </div>
                        <div>
                          <div class="font-semibold text-text-primary">{r.name}</div>
                          <div class="text-[10px] font-mono text-text-secondary">{r.symbol}/USDT</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-3 text-right font-mono text-text-primary">${fmtPrice(r.price)}</td>
                    <td class="px-4 py-3 text-right">
                      <span class={`inline-block px-2 py-0.5 rounded font-mono text-[11px] font-semibold ${
                        r.change >= 0 ? 'bg-accent/15 text-accent' : 'bg-danger/15 text-danger'
                      }`}>
                        {r.change >= 0 ? '+' : ''}{r.change.toFixed(2)}%
                      </span>
                    </td>
                    <td class="px-4 py-3 text-right font-mono text-text-secondary hidden md:table-cell">${r.volume}</td>
                    <td class="px-4 py-3 text-right font-mono text-text-secondary hidden lg:table-cell">${r.mcap}</td>
                    <td class="px-4 py-3 text-right">
                      <button
                        onClick={() => props.onNavigate('page_trade')}
                        class="px-3 py-1.5 text-[11px] font-semibold text-accent bg-accent/10 hover:bg-accent hover:text-background border border-accent/30 rounded transition-all"
                      >
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

      <p class="mt-4 text-[11px] font-mono text-text-secondary">
        Showing {filtered().length} of {rows.length} markets · Prices update every 250ms · Last block: #21,483,207
      </p>
    </div>
  );
}
