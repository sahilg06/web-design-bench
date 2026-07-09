import { createSignal } from 'solid-js';

export default function Contact(props) {
  const [submitted, setSubmitted] = createSignal(false);
  const [form, setForm] = createSignal({
    name: '', email: '', type: 'Brand Identity', budget: '$20k – $40k', message: '',
  });

  const update = (key) => (e) => setForm({ ...form(), [key]: e.currentTarget.value });

  const submit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <>
      <section class="page-intro">
        <div class="container">
          <span class="eyebrow">Get in Touch</span>
          <h1>Let's build something with intention.</h1>
          <p>
            We take on a small number of new engagements each quarter. Tell us
            about your project and we'll be in touch within two business days.
          </p>
        </div>
      </section>

      <section class="section" style="padding-top: 2rem;">
        <div class="container">
          <div class="contact-grid">
            {/* Left: Form */}
            <form class="contact-form" onSubmit={submit}>
              {submitted() && (
                <div
                  style="margin-bottom: 1.5rem; padding: 1rem 1.25rem; border-radius: 10px; background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.4); color: #ff9c6f; font-size: 0.95rem;"
                >
                  Thanks {form().name || 'there'} — your note is on its way. We'll reply within 48 hours.
                </div>
              )}

              <div class="form-row">
                <div class="form-group">
                  <label class="form-label" for="name">Full Name</label>
                  <input
                    id="name"
                    class="form-input"
                    type="text"
                    placeholder="Alex Rivera"
                    value={form().name}
                    onInput={update('name')}
                    required
                  />
                </div>
                <div class="form-group">
                  <label class="form-label" for="email">Email Address</label>
                  <input
                    id="email"
                    class="form-input"
                    type="email"
                    placeholder="alex@company.com"
                    value={form().email}
                    onInput={update('email')}
                    required
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-label" for="type">Project Type</label>
                  <select
                    id="type"
                    class="form-select"
                    value={form().type}
                    onChange={update('type')}
                  >
                    <option>Brand Identity</option>
                    <option>Web Design</option>
                    <option>Mobile App</option>
                    <option>Print & Packaging</option>
                    <option>Strategy & Advisory</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label" for="budget">Budget Range</label>
                  <select
                    id="budget"
                    class="form-select"
                    value={form().budget}
                    onChange={update('budget')}
                  >
                    <option>Under $20k</option>
                    <option>$20k – $40k</option>
                    <option>$40k – $80k</option>
                    <option>$80k – $150k</option>
                    <option>$150k+</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="message">Tell us about your project</label>
                <textarea
                  id="message"
                  class="form-textarea"
                  placeholder="A few sentences about what you're building, your timeline, and where we can help."
                  value={form().message}
                  onInput={update('message')}
                  required
                ></textarea>
              </div>

              <button type="submit" class="btn btn-primary btn-arrow">
                Send Message
              </button>
            </form>

            {/* Right: Info */}
            <aside class="contact-info">
              <div class="info-block">
                <h4>Email</h4>
                <p>hello@aura.studio</p>
                <p class="subtle">For new projects & partnerships</p>
              </div>

              <div class="info-block">
                <h4>Phone</h4>
                <p>+1 (718) 555-0142</p>
                <p class="subtle">Mon–Fri · 9:00am – 6:00pm ET</p>
              </div>

              <div class="info-block">
                <h4>Studio</h4>
                <p>124 Wythe Ave, Floor 3</p>
                <p>Brooklyn, NY 11249</p>
                <p class="subtle">Visits welcome — please book ahead.</p>
              </div>

              <div class="info-block">
                <h4>Office Hours</h4>
                <p>Monday – Friday · 9:00 – 18:00</p>
                <p class="subtle">Weekends by appointment for launches</p>
              </div>

              <div class="info-block">
                <h4>Follow Along</h4>
                <div class="social-links">
                  <a class="social-link" title="Instagram">IG</a>
                  <a class="social-link" title="Dribbble">DR</a>
                  <a class="social-link" title="LinkedIn">LI</a>
                  <a class="social-link" title="Are.na">AN</a>
                  <a class="social-link" title="Twitter/X">X</a>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </section>
    </>
  );
}
