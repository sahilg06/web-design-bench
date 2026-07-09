import { useState } from 'react';
import Home from './pages/Home.jsx';
import Features from './pages/Features.jsx';
import Pricing from './pages/Pricing.jsx';
import About from './pages/About.jsx';
import Contact from './pages/Contact.jsx';

const NAV_ITEMS = [
  { id: 'page_home', label: 'Home' },
  { id: 'page_features', label: 'Features' },
  { id: 'page_pricing', label: 'Pricing' },
  { id: 'page_about', label: 'About' },
  { id: 'page_contact', label: 'Contact' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('page_home');

  const renderPage = () => {
    switch (activeTab) {
      case 'page_features':
        return <Features />;
      case 'page_pricing':
        return <Pricing />;
      case 'page_about':
        return <About />;
      case 'page_contact':
        return <Contact />;
      case 'page_home':
      default:
        return <Home onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="nav-inner">
          <button
            className="brand"
            onClick={() => setActiveTab('page_home')}
            aria-label="Luminary AI Home"
          >
            <span className="brand-logo">L</span>
            <span>Luminary AI</span>
          </button>
          <nav className="nav-links" aria-label="Primary navigation">
            {NAV_ITEMS.map((item) => (
              <button
                key={item.id}
                className={`nav-link ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
              >
                {item.label}
              </button>
            ))}
            <button
              className="nav-cta"
              onClick={() => setActiveTab('page_contact')}
            >
              Book a Demo
            </button>
          </nav>
        </div>
      </header>

      <main>
        <div className="container">{renderPage()}</div>
      </main>

      <footer>
        <div className="footer-inner">
          <div className="footer-grid">
            <div>
              <div className="brand">
                <span className="brand-logo">L</span>
                <span>Luminary AI</span>
              </div>
              <p className="footer-brand-desc">
                Enterprise-grade AI infrastructure powering the next generation of
                intelligent business applications. Trusted by 400+ organizations worldwide.
              </p>
            </div>
            <div className="footer-col">
              <h4>Product</h4>
              <ul>
                <li><a onClick={() => setActiveTab('page_features')}>Features</a></li>
                <li><a onClick={() => setActiveTab('page_pricing')}>Pricing</a></li>
                <li><a onClick={() => setActiveTab('page_features')}>Integrations</a></li>
                <li><a onClick={() => setActiveTab('page_features')}>Changelog</a></li>
              </ul>
            </div>
            <div className="footer-col">
              <h4>Company</h4>
              <ul>
                <li><a onClick={() => setActiveTab('page_about')}>About</a></li>
                <li><a onClick={() => setActiveTab('page_about')}>Team</a></li>
                <li><a onClick={() => setActiveTab('page_contact')}>Careers</a></li>
                <li><a onClick={() => setActiveTab('page_contact')}>Contact</a></li>
              </ul>
            </div>
            <div className="footer-col">
              <h4>Resources</h4>
              <ul>
                <li><a>Documentation</a></li>
                <li><a>API Reference</a></li>
                <li><a>Security</a></li>
                <li><a>Status</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p className="footer-copy">© 2026 Luminary AI, Inc. All rights reserved.</p>
            <div className="footer-legal">
              <a>Privacy</a>
              <a>Terms</a>
              <a>Cookies</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
