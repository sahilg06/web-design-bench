import React, { useState } from 'react';
import Home from './pages/Home.jsx';
import Solutions from './pages/Solutions.jsx';
import Pricing from './pages/Pricing.jsx';
import Docs from './pages/Docs.jsx';
import Contact from './pages/Contact.jsx';

const NAV_ITEMS = [
  { id: 'page_home', label: 'Home' },
  { id: 'page_solutions', label: 'Solutions' },
  { id: 'page_pricing', label: 'Pricing' },
  { id: 'page_docs', label: 'Docs' },
  { id: 'page_contact', label: 'Contact' },
];

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <div className="relative h-9 w-9 grid place-items-center rounded-lg bg-gradient-to-br from-accent to-accentWarm shadow-lg shadow-accent/30">
        <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5 text-slate-900" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7l10 5 10-5-10-5z" fill="currentColor" />
          <path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      <div className="flex flex-col leading-none">
        <span className="text-lg font-bold tracking-tight text-white">Nexus</span>
        <span className="text-[10px] font-medium tracking-[0.2em] text-textSecondary uppercase">SaaS</span>
      </div>
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState('page_home');
  const [mobileOpen, setMobileOpen] = useState(false);

  const renderPage = () => {
    switch (activeTab) {
      case 'page_home': return <Home setActiveTab={setActiveTab} />;
      case 'page_solutions': return <Solutions />;
      case 'page_pricing': return <Pricing />;
      case 'page_docs': return <Docs />;
      case 'page_contact': return <Contact />;
      default: return <Home setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-background text-textPrimary font-sans">
      {/* NAV */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-background/70 border-b border-borderc/60">
        <nav className="max-w-7xl mx-auto px-5 sm:px-8 h-16 flex items-center justify-between">
          <button onClick={() => setActiveTab('page_home')} className="focus:outline-none">
            <Logo />
          </button>

          <ul className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const isActive = activeTab === item.id;
              return (
                <li key={item.id}>
                  <button
                    onClick={() => setActiveTab(item.id)}
                    className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'text-white bg-surface/80'
                        : 'text-textSecondary hover:text-white hover:bg-surface/50'
                    }`}
                  >
                    {item.label}
                    {isActive && (
                      <span className="absolute left-1/2 -bottom-[13px] -translate-x-1/2 h-[2px] w-8 bg-gradient-to-r from-accent to-accentWarm rounded-full"></span>
                    )}
                  </button>
                </li>
              );
            })}
          </ul>

          <div className="hidden md:flex items-center gap-3">
            <button
              onClick={() => setActiveTab('page_contact')}
              className="text-sm font-medium text-textSecondary hover:text-white transition"
            >
              Sign in
            </button>
            <button
              onClick={() => setActiveTab('page_pricing')}
              className="px-4 py-2 rounded-lg text-sm font-semibold text-slate-900 bg-gradient-to-r from-accent to-accentWarm hover:brightness-110 shadow-lg shadow-accent/20 transition"
            >
              Get Started
            </button>
          </div>

          {/* Mobile toggle */}
          <button
            aria-label="Toggle menu"
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden inline-flex items-center justify-center h-10 w-10 rounded-lg bg-surface border border-borderc text-white"
          >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
              {mobileOpen
                ? <path d="M6 6l12 12M6 18L18 6" strokeLinecap="round" />
                : <path d="M4 7h16M4 12h16M4 17h16" strokeLinecap="round" />}
            </svg>
          </button>
        </nav>

        {mobileOpen && (
          <div className="md:hidden border-t border-borderc/60 bg-background/95">
            <ul className="px-5 py-3 flex flex-col gap-1">
              {NAV_ITEMS.map((item) => (
                <li key={item.id}>
                  <button
                    onClick={() => { setActiveTab(item.id); setMobileOpen(false); }}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium ${
                      activeTab === item.id ? 'text-white bg-surface' : 'text-textSecondary'
                    }`}
                  >
                    {item.label}
                  </button>
                </li>
              ))}
              <li className="pt-2">
                <button
                  onClick={() => { setActiveTab('page_pricing'); setMobileOpen(false); }}
                  className="w-full px-4 py-2 rounded-lg text-sm font-semibold text-slate-900 bg-gradient-to-r from-accent to-accentWarm"
                >
                  Get Started
                </button>
              </li>
            </ul>
          </div>
        )}
      </header>

      <main>{renderPage()}</main>

      {/* FOOTER */}
      <footer className="border-t border-borderc/60 bg-surface/30 mt-16">
        <div className="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid grid-cols-2 md:grid-cols-5 gap-8">
          <div className="col-span-2">
            <Logo />
            <p className="mt-4 text-sm text-textSecondary max-w-xs leading-relaxed">
              Connect every tool, workflow, and team on a single unified platform. Trusted by 12,000+ companies worldwide.
            </p>
            <div className="mt-5 flex items-center gap-3">
              {['Twitter', 'GitHub', 'LinkedIn', 'YouTube'].map((s) => (
                <button key={s} aria-label={s} className="h-9 w-9 grid place-items-center rounded-lg bg-surface border border-borderc text-textSecondary hover:text-accent hover:border-accent transition">
                  <span className="text-[10px] font-bold">{s[0]}</span>
                </button>
              ))}
            </div>
          </div>
          {[
            { title: 'Product', links: ['Features', 'Integrations', 'Changelog', 'Roadmap'] },
            { title: 'Company', links: ['About', 'Blog', 'Careers', 'Press Kit'] },
            { title: 'Resources', links: ['Documentation', 'Guides', 'Community', 'Status'] },
          ].map((col) => (
            <div key={col.title}>
              <h4 className="text-xs font-bold tracking-widest text-white uppercase mb-4">{col.title}</h4>
              <ul className="space-y-2.5">
                {col.links.map((l) => (
                  <li key={l}><a href="#" className="text-sm text-textSecondary hover:text-accent transition">{l}</a></li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="border-t border-borderc/60">
          <div className="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col md:flex-row items-center justify-between gap-3">
            <p className="text-xs text-textSecondary">© 2026 Nexus SaaS, Inc. All rights reserved.</p>
            <div className="flex items-center gap-6 text-xs text-textSecondary">
              <a href="#" className="hover:text-white transition">Privacy</a>
              <a href="#" className="hover:text-white transition">Terms</a>
              <a href="#" className="hover:text-white transition">Security</a>
              <a href="#" className="hover:text-white transition">Cookies</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
