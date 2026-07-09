import { createSignal, For } from 'solid-js';

export default function Trade() {
  const [side, setSide] = createSignal('buy');
  const [orderType, setOrderType] = createSignal('limit');
  const [price, setPrice] = createSignal('68412.90');
  const [amount, setAmount] = createSignal('');
  const [pct, setPct] = createSignal(0);

  const asks = [
    { price: 68420.10, amount: 0.412, total: 28189.06 },
    { price: 68419.40, amount: 0.184, total: 12589.17 },
    { price: 68418.80, amount: 1.021, total: 69835.60 },
    { price: 68417.20, amount: 0.542, total: 37082.13 },
    { price: 68416.50, amount: 0.322, total: 22030.11 },
    { price: 68415.90, amount: 0.884, total: 60479.66 },
    { price: 68415.10, amount: 0.212, total: 14504.00 },
    { price: 68414.60, amount: 0.078, total: 5336.33 },
  ];

  const bids = [
    { price: 68411.20, amount: 0.144, total: 9851.21 },
    { price: 68410.50, amount: 0.612, total: 41867.23 },
    { price: 68409.80, amount: 0.288, total: 19702.02 },
    { price: 68408.10, amount: 1.104, total: 75522.54 },
    { price: 68407.20, amount: 0.412, total: 28183.77 },
    { price: 68405.60, amount: 0.192, total: 13133.88 },
    { price: 68404.10, amount: 0.828, total: 56638.59 },
    { price: 68402.80, amount: 0.412, total: 28181.95 },
  ];

  const trades = [
    { time: '14:32:18', price: 68412.90, amount: 0.024, up: true },
    { time: '14:32:16', price: 68411.20, amount: 0.184, up: false },
    { time: '14:32:14', price: 68412.10, amount: 0.062, up: true },
    { time: '14:32:12', price: 68410.80, amount: 0.412, up: false },
    { time: '14:32:10', price: 68411.90, amount: 0.028, up: true },
    { time: '14:32:08', price: 68412.40, amount: 0.144, up: true },
    { time: '14:32:04', price: 68411.10, amount: 0.088, up: false },
    { time: '14:32:01', price: 68412.20, amount: 0.216, up: true },
    { time: '14:31:58', price: 68411.60, amount: 0.062, up: false },
    { time: '14:31:54', price: 68412.90, amount: 0.184, up: true },
  ];

  const maxTotal = Math.max(...asks.map(a => a.total), ...bids.map(b => b.total));

  return (
    <div class="max-w-[1600px] mx-auto px-3 sm:px-4 py-4">
      {/* Symbol header */}
      <div class="bg-surface border border-border rounded-lg mb-3 px-4 py-3">
        <div class="flex flex-wrap items-center gap-6">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-amber-500 flex items-center justify-center text-background text-[11px] font-bold">BTC</div>
            <div>
              <div class="text-base font-bold text-text-primary">BTC/USDT</div>
              <div class="text-[10px] font-mono text-text-secondary">Bitcoin · Perpetual Available</div>
            </div>
          </div>
          <div>
            <div class="text-xl font-bold font-mono text-accent">$68,412.90</div>
            <div class="text-[10px] font-mono text-accent">+2.14% · +$1,438.20</div>
          </div>
          <div class="hidden md:block">
            <div class="text-[10px] font-mono text-text-secondary uppercase">24h High</div>
            <div class="text-sm font-mono text-text-primary">$69,204.10</div>
          </div>
          <div class="hidden md:block">
            <div class="text-[10px] font-mono text-text-secondary uppercase">24h Low</div>
            <div class="text-sm font-mono text-text-primary">$66,812.40</div>
          </div>
          <div class="hidden lg:block">
            <div class="text-[10px] font-mono text-text-secondary uppercase">24h Volume (BTC)</div>
            <div class="text-sm font-mono text-text-primary">414,822.18</div>
          </div>
          <div class="hidden lg:block">
            <div class="text-[10px] font-mono text-text-secondary uppercase">Funding / Countdown</div>
            <div class="text-sm font-mono text-accent">0.0102% / 04:12:41</div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-3">
        {/* Chart column */}
        <section class="lg:col-span-7 space-y-3">
          <div class="bg-surface border border-border rounded-lg overflow-hidden">
            <div class="flex items-center justify-between px-4 py-2 border-b border-border">
              <div class="flex items-center gap-1">
                <For each={['1m', '5m', '15m', '1H', '4H', '1D', '1W']}>
                  {(t, i) => (
                    <button class={`px-2.5 py-1 text-[11px] font-mono rounded ${i() === 3 ? 'bg-accent/15 text-accent' : 'text-text-secondary hover:text-text-primary'}`}>
                      {t}
                    </button>
                  )}
                </For>
              </div>
              <div class="flex items-center gap-3 text-[10px] font-mono text-text-secondary">
                <span>O 68,201.40</span>
                <span>H 68,904.20</span>
                <span>L 68,088.10</span>
                <span class="text-accent">C 68,412.90</span>
              </div>
            </div>
            <div class="relative h-96 grid-bg">
              <svg viewBox="0 0 800 400" preserveAspectRatio="none" class="w-full h-full">
                <defs>
                  <linearGradient id="chartArea" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="#10b981" stop-opacity="0.35" />
                    <stop offset="100%" stop-color="#10b981" stop-opacity="0" />
                  </linearGradient>
                </defs>
                {/* Grid lines */}
                <For each={[0.2, 0.4, 0.6, 0.8]}>
                  {(y) => (
                    <line x1="0" x2="800" y1={400 * y} y2={400 * y} stroke="#27272a" stroke-width="0.5" stroke-dasharray="3 3"/>
                  )}
                </For>
                <path
                  d="M0,320 L40,300 L80,310 L120,285 L160,260 L200,272 L240,240 L280,255 L320,215 L360,228 L400,190 L440,205 L480,168 L520,182 L560,150 L600,165 L640,128 L680,142 L720,105 L760,120 L800,88 L800,400 L0,400 Z"
                  fill="url(#chartArea)"
                />
                <path
                  d="M0,320 L40,300 L80,310 L120,285 L160,260 L200,272 L240,240 L280,255 L320,215 L360,228 L400,190 L440,205 L480,168 L520,182 L560,150 L600,165 L640,128 L680,142 L720,105 L760,120 L800,88"
                  fill="none"
                  stroke="#10b981"
                  stroke-width="2"
                />
                {/* Candles */}
                <For each={[[100, 280, 260, 292, true], [180, 250, 235, 268, true], [260, 232, 218, 245, true], [340, 210, 195, 222, true], [420, 178, 195, 202, false], [500, 165, 148, 178, true], [580, 152, 165, 175, false], [660, 130, 118, 142, true], [740, 108, 92, 118, true]]}>
                  {(c) => (
                    <>
                      <line x1={c[0]} x2={c[0]} y1={c[3] - 12} y2={c[3] + 8} stroke={c[4] ? '#10b981' : '#ef4444'} stroke-width="1"/>
                      <rect x={c[0] - 6} y={Math.min(c[1], c[2])} width="12" height={Math.abs(c[2] - c[1])} fill={c[4] ? '#10b981' : '#ef4444'}/>
                    </>
                  )}
                </For>
              </svg>
              <div class="absolute right-2 top-2 px-2 py-1 bg-background/80 backdrop-blur border border-border rounded text-[10px] font-mono text-accent">
                68,412.90 ▲
              </div>
            </div>
          </div>

          {/* Recent trades */}
          <div class="bg-surface border border-border rounded-lg overflow-hidden">
            <div class="px-4 py-2 border-b border-border flex items-center justify-between">
              <h3 class="text-[11px] font-semibold text-text-secondary uppercase tracking-widest">Recent Trades</h3>
              <span class="text-[10px] font-mono text-accent">● streaming</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-[12px] font-mono">
                <thead>
                  <tr class="text-[10px] text-text-secondary uppercase">
                    <th class="text-left px-4 py-1.5 font-semibold">Time</th>
                    <th class="text-right px-4 py-1.5 font-semibold">Price (USDT)</th>
                    <th class="text-right px-4 py-1.5 font-semibold">Amount (BTC)</th>
                    <th class="text-right px-4 py-1.5 font-semibold">Total (USDT)</th>
                    <th class="text-right px-4 py-1.5 font-semibold">Side</th>
                  </tr>
                </thead>
                <tbody>
                  <For each={trades}>
                    {(t) => (
                      <tr class="hover:bg-background/40">
                        <td class="px-4 py-1 text-text-secondary">{t.time}</td>
                        <td class={`px-4 py-1 text-right ${t.up ? 'text-accent' : 'text-danger'}`}>{t.price.toFixed(2)}</td>
                        <td class="px-4 py-1 text-right text-text-primary">{t.amount.toFixed(3)}</td>
                        <td class="px-4 py-1 text-right text-text-secondary">{(t.price * t.amount).toFixed(2)}</td>
                        <td class={`px-4 py-1 text-right ${t.up ? 'text-accent' : 'text-danger'}`}>{t.up ? 'BUY' : 'SELL'}</td>
                      </tr>
                    )}
                  </For>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Order book column */}
        <section class="lg:col-span-3">
          <div class="bg-surface border border-border rounded-lg overflow-hidden h-full">
            <div class="px-4 py-2 border-b border-border flex items-center justify-between">
              <h3 class="text-[11px] font-semibold text-text-secondary uppercase tracking-widest">Order Book</h3>
              <span class="text-[10px] font-mono text-text-secondary">0.10 ▾</span>
            </div>
            <div class="px-4 py-1.5 grid grid-cols-3 text-[10px] font-mono text-text-secondary uppercase border-b border-border/50">
              <span>Price</span>
              <span class="text-right">Amount</span>
              <span class="text-right">Total</span>
            </div>

            {/* Asks (sells) */}
            <div class="py-1">
              <For each={asks.slice().reverse()}>
                {(a) => (
                  <div class="relative px-4 py-[3px] grid grid-cols-3 text-[11px] font-mono hover:bg-danger/5 cursor-pointer">
                    <div class="absolute right-0 top-0 h-full bg-danger/10" style={{ width: `${(a.total / maxTotal) * 100}%` }}></div>
                    <span class="relative text-danger">{a.price.toFixed(2)}</span>
                    <span class="relative text-right text-text-primary">{a.amount.toFixed(3)}</span>
                    <span class="relative text-right text-text-secondary">{a.total.toFixed(2)}</span>
                  </div>
                )}
              </For>
            </div>

            {/* Spread */}
            <div class="px-4 py-2 border-y border-border bg-background/40 flex items-center justify-between">
              <div>
                <div class="text-lg font-bold font-mono text-accent">68,412.90</div>
                <div class="text-[10px] font-mono text-text-secondary">≈ $68,412.90</div>
              </div>
              <div class="text-right">
                <div class="text-[10px] font-mono text-text-secondary uppercase">Spread</div>
                <div class="text-[11px] font-mono text-text-primary">3.40 (0.005%)</div>
              </div>
            </div>

            {/* Bids (buys) */}
            <div class="py-1">
              <For each={bids}>
                {(b) => (
                  <div class="relative px-4 py-[3px] grid grid-cols-3 text-[11px] font-mono hover:bg-accent/5 cursor-pointer">
                    <div class="absolute right-0 top-0 h-full bg-accent/10" style={{ width: `${(b.total / maxTotal) * 100}%` }}></div>
                    <span class="relative text-accent">{b.price.toFixed(2)}</span>
                    <span class="relative text-right text-text-primary">{b.amount.toFixed(3)}</span>
                    <span class="relative text-right text-text-secondary">{b.total.toFixed(2)}</span>
                  </div>
                )}
              </For>
            </div>
          </div>
        </section>

        {/* Order form column */}
        <section class="lg:col-span-2">
          <div class="bg-surface border border-border rounded-lg overflow-hidden">
            {/* Side tabs */}
            <div class="grid grid-cols-2">
              <button
                onClick={() => setSide('buy')}
                class={`py-3 text-sm font-semibold transition-all ${
                  side() === 'buy'
                    ? 'bg-accent text-background shadow-glow-accent'
                    : 'bg-background/40 text-text-secondary hover:text-text-primary'
                }`}
              >
                Buy / Long
              </button>
              <button
                onClick={() => setSide('sell')}
                class={`py-3 text-sm font-semibold transition-all ${
                  side() === 'sell'
                    ? 'bg-danger text-background'
                    : 'bg-background/40 text-text-secondary hover:text-text-primary'
                }`}
              >
                Sell / Short
              </button>
            </div>

            <div class="p-4 space-y-3">
              {/* Type tabs */}
              <div class="flex gap-1 border-b border-border pb-2">
                <For each={['limit', 'market', 'stop']}>
                  {(t) => (
                    <button
                      onClick={() => setOrderType(t)}
                      class={`px-3 py-1 text-[11px] font-semibold uppercase tracking-wider rounded ${
                        orderType() === t ? 'text-accent bg-accent/10' : 'text-text-secondary hover:text-text-primary'
                      }`}
                    >
                      {t}
                    </button>
                  )}
                </For>
              </div>

              {/* Available */}
              <div class="flex justify-between text-[11px] font-mono">
                <span class="text-text-secondary">Available</span>
                <span class="text-text-primary">12,418.44 USDT</span>
              </div>

              {/* Price */}
              <div>
                <label class="text-[10px] font-mono text-text-secondary uppercase">Limit Price</label>
                <div class="mt-1 flex items-center bg-background border border-border rounded-md px-3 py-2 focus-within:border-accent/60">
                  <input
                    type="text"
                    value={price()}
                    onInput={(e) => setPrice(e.currentTarget.value)}
                    class="flex-1 bg-transparent text-sm font-mono text-text-primary focus:outline-none"
                  />
                  <span class="text-[10px] font-mono text-text-secondary">USDT</span>
                </div>
              </div>

              {/* Amount */}
              <div>
                <label class="text-[10px] font-mono text-text-secondary uppercase">Amount</label>
                <div class="mt-1 flex items-center bg-background border border-border rounded-md px-3 py-2 focus-within:border-accent/60">
                  <input
                    type="text"
                    value={amount()}
                    onInput={(e) => setAmount(e.currentTarget.value)}
                    placeholder="0.00"
                    class="flex-1 bg-transparent text-sm font-mono text-text-primary placeholder:text-text-secondary focus:outline-none"
                  />
                  <span class="text-[10px] font-mono text-text-secondary">BTC</span>
                </div>
              </div>

              {/* Percentage slider */}
              <div>
                <div class="flex justify-between text-[10px] font-mono text-text-secondary mb-1">
                  <span>0%</span>
                  <span class="text-accent">{pct()}%</span>
                  <span>100%</span>
                </div>
                <div class="relative h-1.5 bg-background rounded-full">
                  <div class="absolute inset-y-0 left-0 bg-accent rounded-full" style={{ width: `${pct()}%` }}></div>
                </div>
                <div class="grid grid-cols-4 gap-1 mt-2">
                  <For each={[25, 50, 75, 100]}>
                    {(p) => (
                      <button
                        onClick={() => setPct(p)}
                        class="py-1 text-[10px] font-mono text-text-secondary bg-background border border-border rounded hover:text-accent hover:border-accent/40"
                      >
                        {p}%
                      </button>
                    )}
                  </For>
                </div>
              </div>

              {/* Total */}
              <div class="pt-2 border-t border-border space-y-1">
                <div class="flex justify-between text-[11px] font-mono">
                  <span class="text-text-secondary">Order Value</span>
                  <span class="text-text-primary">{amount() && price() ? (parseFloat(price()) * parseFloat(amount() || 0)).toFixed(2) : '0.00'} USDT</span>
                </div>
                <div class="flex justify-between text-[11px] font-mono">
                  <span class="text-text-secondary">Fee (0.02%)</span>
                  <span class="text-text-primary">{amount() && price() ? (parseFloat(price()) * parseFloat(amount() || 0) * 0.0002).toFixed(4) : '0.00'} USDT</span>
                </div>
              </div>

              {/* Submit */}
              <button
                class={`w-full py-3 text-sm font-bold rounded-md transition-all ${
                  side() === 'buy'
                    ? 'bg-accent hover:bg-emerald-400 text-background shadow-glow-accent'
                    : 'bg-danger hover:bg-red-400 text-background'
                }`}
              >
                {side() === 'buy' ? 'Place Buy Order' : 'Place Sell Order'}
              </button>

              <div class="pt-2 text-center">
                <span class="text-[10px] font-mono text-text-secondary">Est. execution: </span>
                <span class="text-[10px] font-mono text-accent">98ms</span>
              </div>
            </div>
          </div>

          {/* Open orders (placeholder) */}
          <div class="mt-3 bg-surface border border-border rounded-lg p-4">
            <h3 class="text-[11px] font-semibold text-text-secondary uppercase tracking-widest mb-3">Your Positions</h3>
            <div class="space-y-2 text-[11px] font-mono">
              <div class="flex justify-between">
                <span class="text-text-secondary">BTC/USDT Long</span>
                <span class="text-accent">+$412.90</span>
              </div>
              <div class="flex justify-between">
                <span class="text-text-secondary">ETH/USDT Long</span>
                <span class="text-accent">+$88.12</span>
              </div>
              <div class="flex justify-between">
                <span class="text-text-secondary">SOL/USDT Short</span>
                <span class="text-danger">-$14.40</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
