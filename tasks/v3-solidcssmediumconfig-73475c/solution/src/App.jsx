import { createSignal, Match, Switch } from 'solid-js';
import Home from './pages/Home';
import Work from './pages/Work';
import Services from './pages/Services';
import About from './pages/About';
import Contact from './pages/Contact';

const NAV = [
  { key: 'page_home', label: 'Home' },
  { key: 'page_work', label: 'Work' },
  { key: 'page_services', label: 'Services' },
  { key: 'page_about', label: 'About' },
  { key: 'page_contact', label: 'Contact' },
];

export default function App() {
  const [activeTab, setActiveTab] = createSignal('page_home');

  const go = (key) => {
    setActiveTab(key);
    if (typeof window !== 'undefined') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <>
      <header class="nav">
        <div class="nav-inner">
          <div class="brand" onClick={() => go('page_home')}>
            <div class="brand-mark">A</div>
            <div class="brand-name">Aura<span>.</span></div>
          </div>

          <nav class="nav-links" aria-label="Primary">
            {NAV.map((item) => (
              <button
                class={`nav-link ${activeTab() === item.key ? 'active' : ''}`}
                onClick={() => go(item.key)}
              >
                {item.label}
              </button>
            ))}
            <button
              class="btn btn-primary nav-cta"
              onClick={() => go('page_contact')}
            >
              Start a Project
            </button>
          </nav>
        </div>
      </header>

      <main>
        <Switch>
          <Match when={activeTab() === 'page_home'}>
            <Home go={go} />
          </Match>
          <Match when={activeTab() === 'page_work'}>
            <Work go={go} />
          </Match>
          <Match when={activeTab() === 'page_services'}>
            <Services go={go} />
          </Match>
          <Match when={activeTab() === 'page_about'}>
            <About go={go} />
          </Match>
          <Match when={activeTab() === 'page_contact'}>
            <Contact go={go} />
          </Match>
        </Switch>
      </main>

      <footer class="footer">
        <div class="container">
          <div class="footer-grid">
            <div class="footer-col footer-brand">
              <div class="brand">
                <div class="brand-mark">A</div>
                <div class="brand-name">Aura<span>.</span> Creative</div>
              </div>
              <p>
                An independent design studio building brands, digital products, and
                cultural artifacts from Brooklyn, NY.
              </p>
            </div>

            <div class="footer-col">
              <h5>Studio</h5>
              <ul class="footer-list">
                <li><button onClick={() => go('page_about')}>About</button></li>
                <li><button onClick={() => go('page_services')}>Services</button></li>
                <li><button onClick={() => go('page_work')}>Work</button></li>
                <li><button onClick={() => go('page_contact')}>Contact</button></li>
              </ul>
            </div>

            <div class="footer-col">
              <h5>Say Hello</h5>
              <ul class="footer-list">
                <li><button>hello@aura.studio</button></li>
                <li><button>+1 (718) 555-0142</button></li>
                <li><button>124 Wythe Ave, Brooklyn</button></li>
              </ul>
            </div>
          </div>

          <div class="footer-bottom">
            <span>© 2026 Aura Creative Studio. All rights reserved.</span>
            <span>Crafted with intention in Brooklyn, NY.</span>
          </div>
        </div>
      </footer>
    </>
  );
}
