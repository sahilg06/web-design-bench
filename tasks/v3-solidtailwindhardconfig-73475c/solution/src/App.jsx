import { createSignal } from 'solid-js';
import Home from './pages/Home';
import Markets from './pages/Markets';
import Trade from './pages/Trade';
import Earn from './pages/Earn';
import Wallet from './pages/Wallet';

export default function App() {
  const [activeTab, setActiveTab] = createSignal('page_home');
  const [menuOpen, setMenuOpen] = createSignal(false);

  const tabs = [
    { id: 'page_home', label: 'Home' },
    { id: 'page_markets', label: 'Markets' },
    { id: 'page_trade', label: 'Trade' },
    { id: 'page_earn', label: 'Earn' },
    { id: 'page_wallet', label: 'Wallet' },
  ];

  const navClick = (id) => {
    setActiveTab(id);
    setMenuOpen(false);
    if (typeof window !== 'undefined') window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div class="min-h-screen bg-background text-text-primary flex flex-col">
      <nav class="sticky top-0 z-50 bg-background/85 backdrop-blur-xl border-b border-border">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between h-16">
            <div class="flex items-center gap-10">
              <button onClick={() => navClick('page_home')} class="flex items-center gap-2.5 group">
                <div class="w-8 h-8 rounded-md bg-gradient-to-br from-accent to-emerald-700 flex items-center justify-center shadow-glow-accent">
                  <svg width="18" height="18" viewBox="0 0 32 32" fill="none">
                    <path d="M8 16 L14 10 L14 14 L24 14 L24 18 L14 18 L14 22 Z" fill="#09090b"/>
                  </svg>
                </div>
                <div class="flex items-baseline gap-1.5">
                  <span class="text-lg font-bold tracking-tight">Cypher</span>
                  <span class="text-[10px] font-mono text-accent tracking-[0.2em]">DEX</span>
                </div>
              </button>
              <div class="hidden md:flex items-center gap-1">
                {tabs.map((t) => (
                  <button
                    onClick={() => navClick(t.id)}
                    class={`px-3.5 py-1.5 text-sm font-medium rounded-md transition-all ${
                      activeTab() === t.id
                        ? 'text-accent bg-accent/10 ring-1 ring-accent/30'
                        : 'text-text-secondary hover:text-text-primary hover:bg-surface'
                    }`}
                  >
                    {t.label}
                  </button>
                ))}
              </div>
            </div>

            <div class="hidden md:flex items-center gap-3">
              <div class="flex items-center gap-2 px-3 py-1.5 bg-surface border border-border rounded-md">
                <span class="w-1.5 h-1.5 rounded-full bg-accent pulse-dot"></span>
                <span class="text-[11px] font-mono text-text-secondary">MAINNET</span>
              </div>
              <button class="px-3.5 py-1.5 text-sm font-medium text-text-secondary hover:text-text-primary border border-border rounded-md hover:border-zinc-600 transition-colors">
                0x4a9F...3bE1
              </button>
              <button class="px-4 py-1.5 text-sm font-semibold text-background bg-accent hover:bg-emerald-400 rounded-md transition-all shadow-glow-accent hover:shadow-emerald-500/50">
                Connect Wallet
              </button>
            </div>

            <button
              onClick={() => setMenuOpen(!menuOpen())}
              class="md:hidden p-2 text-text-secondary hover:text-text-primary"
              aria-label="Toggle menu"
            >
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                {menuOpen()
                  ? <path d="M6 6l12 12M6 18L18 6" />
                  : <path d="M4 7h16M4 12h16M4 17h16" />}
              </svg>
            </button>
          </div>

          {menuOpen() && (
            <div class="md:hidden border-t border-border py-3 space-y-1">
              {tabs.map((t) => (
                <button
                  onClick={() => navClick(t.id)}
                  class={`w-full text-left px-3 py-2 text-sm font-medium rounded-md ${
                    activeTab() === t.id
                      ? 'text-accent bg-accent/10'
                      : 'text-text-secondary hover:text-text-primary hover:bg-surface'
                  }`}
                >
                  {t.label}
                </button>
              ))}
              <button class="w-full mt-2 px-4 py-2 text-sm font-semibold text-background bg-accent rounded-md">
                Connect Wallet
              </button>
            </div>
          )}
        </div>
      </nav>

      <main class="flex-1">
        {activeTab() === 'page_home' && <Home onNavigate={navClick} />}
        {activeTab() === 'page_markets' && <Markets onNavigate={navClick} />}
        {activeTab() === 'page_trade' && <Trade />}
        {activeTab() === 'page_earn' && <Earn />}
        {activeTab() === 'page_wallet' && <Wallet />}
      </main>

      <footer class="border-t border-border bg-background">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
          <div class="grid grid-cols-2 md:grid-cols-5 gap-10">
            <div class="col-span-2">
              <div class="flex items-center gap-2.5 mb-4">
                <div class="w-8 h-8 rounded-md bg-gradient-to-br from-accent to-emerald-700 flex items-center justify-center">
                  <svg width="18" height="18" viewBox="0 0 32 32" fill="none">
                    <path d="M8 16 L14 10 L14 14 L24 14 L24 18 L14 18 L14 22 Z" fill="#09090b"/>
                  </svg>
                </div>
                <span class="text-lg font-bold">Cypher DEX</span>
              </div>
              <p class="text-sm text-text-secondary max-w-sm leading-relaxed">
                A permissionless, non-custodial decentralized exchange engineered for sub-100ms order execution across 14 blockchains.
              </p>
              <div class="mt-5 flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-accent pulse-dot"></span>
                <span class="text-[11px] font-mono text-text-secondary">All systems operational</span>
              </div>
            </div>
            <div>
              <h4 class="text-[11px] font-semibold text-text-secondary uppercase tracking-widest mb-4">Product</h4>
              <ul class="space-y-2.5 text-sm text-text-secondary">
                <li class="hover:text-accent cursor-pointer transition-colors">Spot Trading</li>
                <li class="hover:text-accent cursor-pointer transition-colors">Perpetuals</li>
                <li class="hover:text-accent cursor-pointer transition-colors">Yield Farming</li>
                <li class="hover:text-accent cursor-pointer transition-colors">Liquidity Pools</li>
              </ul>
            </div>
            <div>
              <h4 class="text-[11px] font-semibold text-text-secondary uppercase tracking-widest mb-4">Developers</h4>
              <ul class="space-y-2.5 text-sm text-text-secondary">
                <li class="hover:text-accent cursor-pointer transition-colors">Documentation</li>
                <li class="hover:text-accent cursor-pointer transition-colors">API Reference</li>
                <li class="hover:text-accent cursor-pointer transition-colors">GitHub</li>
                <li class="hover:text-accent cursor-pointer transition-colors">Bug Bounty</li>
              </ul>
            </div>
            <div>
              <h4 class="text-[11px] font-semibold text-text-secondary uppercase tracking-widest mb-4">Community</h4>
              <ul class="space-y-2.5 text-sm text-text-secondary">
                <li class="hover:text-accent cursor-pointer transition-colors">Discord</li>
                <li class="hover:text-accent cursor-pointer transition-colors">Twitter / X</li>
                <li class="hover:text-accent cursor-pointer transition-colors">Governance</li>
                <li class="hover:text-accent cursor-pointer transition-colors">Blog</li>
              </ul>
            </div>
          </div>
          <div class="mt-12 pt-6 border-t border-border flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
            <p class="text-xs text-text-secondary font-mono">
              © 2026 Cypher Labs — Audited by Trail of Bits &amp; OpenZeppelin
            </p>
            <div class="flex items-center gap-5 text-xs text-text-secondary">
              <span class="hover:text-text-primary cursor-pointer">Terms</span>
              <span class="hover:text-text-primary cursor-pointer">Privacy</span>
              <span class="hover:text-text-primary cursor-pointer">Risk Disclosure</span>
              <span class="font-mono text-accent">v4.2.1</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
