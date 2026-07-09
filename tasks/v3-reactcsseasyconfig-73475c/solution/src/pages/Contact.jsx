import { useState } from 'react';

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    setForm({ name: '', email: '', message: '' });
    setTimeout(() => setSubmitted(false), 5000);
  };

  return (
    <>
      <div className="section-header">
        <div className="section-eyebrow">Get in Touch</div>
        <h2>Let's talk about your project</h2>
        <p>
          Whether you're evaluating platforms, planning a rollout, or just curious
          about what's possible — our team responds within one business day.
        </p>
      </div>

      <div className="contact-layout">
        <form className="contact-form" onSubmit={handleSubmit}>
          <h2>Send us a message</h2>
          <p className="contact-form-lead">
            Fill in a few details and we'll route your inquiry to the right person on our team.
          </p>

          <div className="form-group">
            <label htmlFor="name" className="form-label">Full name</label>
            <input
              type="text"
              id="name"
              name="name"
              className="form-input"
              placeholder="Jamie Rivera"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email" className="form-label">Work email</label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-input"
              placeholder="jamie@company.com"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="message" className="form-label">How can we help?</label>
            <textarea
              id="message"
              name="message"
              className="form-textarea"
              placeholder="Tell us about your use case, team size, and timeline..."
              value={form.message}
              onChange={handleChange}
              required
            ></textarea>
          </div>

          <button type="submit" className="btn btn-primary btn-lg">
            Send Message
          </button>

          {submitted && (
            <div className="form-success">
              ✓ Thanks — we received your message and will reply within 24 hours.
            </div>
          )}
        </form>

        <aside className="contact-sidebar">
          <div className="contact-card">
            <div className="contact-card-icon">📍</div>
            <h3>Headquarters</h3>
            <p>
              440 Bryant Street, Suite 300<br />
              San Francisco, CA 94107<br />
              United States
            </p>
            <div className="map-placeholder" aria-hidden="true">
              <div className="map-pin"></div>
            </div>
          </div>

          <div className="contact-card">
            <div className="contact-card-icon">✉</div>
            <h3>Direct channels</h3>
            <p>
              Sales: <a href="mailto:hello@luminary.ai">hello@luminary.ai</a><br />
              Support: <a href="mailto:support@luminary.ai">support@luminary.ai</a><br />
              Press: <a href="mailto:press@luminary.ai">press@luminary.ai</a>
            </p>
          </div>

          <div className="contact-card">
            <div className="contact-card-icon">☎</div>
            <h3>Enterprise sales</h3>
            <p>
              For teams over 500 seats or regulated industries:<br />
              <a href="tel:+14155550142">+1 (415) 555-0142</a><br />
              Mon–Fri, 8am–6pm PT
            </p>
          </div>
        </aside>
      </div>
    </>
  );
}
