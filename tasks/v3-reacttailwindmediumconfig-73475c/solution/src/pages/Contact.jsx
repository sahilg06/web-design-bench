import React, { useState } from 'react';

export default function Contact() {
  const [form, setForm] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    role: '',
    size: '10-50',
    interest: 'Pro plan',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const update = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  const submit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="relative overflow-hidden">
      <div className="absolute top-0 left-1/4 h-96 w-96 rounded-full bg-accent/15 blur-3xl"></div>
      <div className="absolute top-40 right-1/4 h-96 w-96 rounded-full bg-accentWarm/15 blur-3xl"></div>

      <div className="relative max-w-7xl mx-auto px-5 sm:px-8 py-16 md:py-20">
        <div className="text-center mb-14">
          <span className="text-xs font-bold tracking-widest text-accent uppercase">Contact Sales</span>
          <h1 className="mt-3 text-4xl md:text-6xl font-black tracking-tight text-white">
            Let's build{' '}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-accent to-accentWarm">something serious</span>
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-lg text-textSecondary">
            Tell us about your integration needs. Our solutions team responds within one business day — usually much faster.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16">
          {/* LEFT: SALES INFO */}
          <div>
            <div className="rounded-2xl bg-surface/60 border border-borderc p-6 md:p-8">
              <h3 className="text-xl font-bold text-white">What to expect</h3>
              <ul className="mt-5 space-y-4">
                {[
                  { t: 'A 20-minute discovery call', d: 'We map your integration needs and compliance requirements before pitching anything.' },
                  { t: 'A custom architecture review', d: 'Our solutions engineers sketch a plan for your specific stack and data flows.' },
                  { t: 'A sandbox for your team', d: 'Two-week access to a dedicated Nexus workspace, pre-loaded with your integrations.' },
                  { t: 'A ROI model — not a slide deck', d: 'We show the payback math against your current tooling spend.' },
                ].map((s, i) => (
                  <li key={s.t} className="flex gap-4">
                    <div className="shrink-0 h-8 w-8 rounded-lg bg-gradient-to-br from-accent to-accentWarm text-slate-900 font-bold grid place-items-center">
                      {i + 1}
                    </div>
                    <div>
                      <div className="font-semibold text-white">{s.t}</div>
                      <div className="text-sm text-textSecondary mt-0.5">{s.d}</div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="rounded-2xl bg-surface/40 border border-borderc p-5">
                <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase">Enterprise sales</div>
                <div className="mt-2 text-white font-semibold">sales@nexus.io</div>
                <div className="text-sm text-textSecondary">+1 (415) 555-0198</div>
              </div>
              <div className="rounded-2xl bg-surface/40 border border-borderc p-5">
                <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase">Partnerships</div>
                <div className="mt-2 text-white font-semibold">partners@nexus.io</div>
                <div className="text-sm text-textSecondary">+1 (415) 555-0142</div>
              </div>
            </div>

            <div className="mt-6 rounded-2xl bg-gradient-to-br from-accent/10 to-accentWarm/10 border border-accent/30 p-5 md:p-6">
              <div className="flex items-start gap-4">
                <div className="h-12 w-12 rounded-full bg-gradient-to-br from-accent to-accentWarm shrink-0"></div>
                <div>
                  <blockquote className="text-textPrimary italic">
                    "The Nexus solutions team spent three calls on our data model before quoting anything. Refreshing after a decade of vendor demos."
                  </blockquote>
                  <div className="mt-3 text-sm">
                    <span className="text-white font-semibold">Lena Alvarez</span>
                    <span className="text-textSecondary"> · Director of Integration, Vector.io</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 rounded-2xl bg-surface/40 border border-borderc p-5 md:p-6">
              <div className="text-[10px] font-bold tracking-widest text-textSecondary uppercase mb-3">Global offices</div>
              <div className="grid grid-cols-3 gap-4 text-sm">
                {[
                  { c: 'San Francisco', a: '535 Mission St.' },
                  { c: 'London', a: '10 Finsbury Sq.' },
                  { c: 'Singapore', a: '1 Raffles Pl.' },
                ].map((o) => (
                  <div key={o.c}>
                    <div className="font-semibold text-white">{o.c}</div>
                    <div className="text-textSecondary text-xs mt-0.5">{o.a}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* RIGHT: FORM */}
          <div className="relative">
            <div className="absolute -inset-4 bg-gradient-to-br from-accent/20 via-transparent to-accentWarm/20 blur-2xl opacity-60"></div>
            <div className="relative rounded-2xl bg-surface border border-borderc p-6 md:p-8 shadow-2xl shadow-accent/10">
              {submitted ? (
                <div className="text-center py-12">
                  <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-br from-accent to-accentWarm grid place-items-center text-slate-900 text-3xl font-black">✓</div>
                  <h3 className="mt-5 text-2xl font-bold text-white">Message received</h3>
                  <p className="mt-2 text-textSecondary">
                    Thanks, {form.firstName || 'friend'}. A solutions engineer will reach out at{' '}
                    <span className="text-accent font-mono">{form.email || 'your address'}</span> within one business day.
                  </p>
                  <button
                    onClick={() => { setSubmitted(false); setForm({ firstName: '', lastName: '', email: '', company: '', role: '', size: '10-50', interest: 'Pro plan', message: '' }); }}
                    className="mt-6 text-sm font-semibold text-accent hover:text-white transition"
                  >
                    Send another message →
                  </button>
                </div>
              ) : (
                <form onSubmit={submit} className="space-y-5">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">First name</label>
                      <input
                        required
                        value={form.firstName}
                        onChange={update('firstName')}
                        placeholder="Ada"
                        className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white placeholder:text-textSecondary/60 focus:border-accent focus:outline-none transition"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">Last name</label>
                      <input
                        required
                        value={form.lastName}
                        onChange={update('lastName')}
                        placeholder="Lovelace"
                        className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white placeholder:text-textSecondary/60 focus:border-accent focus:outline-none transition"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">Work email</label>
                    <input
                      required
                      type="email"
                      value={form.email}
                      onChange={update('email')}
                      placeholder="ada@company.com"
                      className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white placeholder:text-textSecondary/60 focus:border-accent focus:outline-none transition"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">Company</label>
                      <input
                        required
                        value={form.company}
                        onChange={update('company')}
                        placeholder="Atlas Corp"
                        className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white placeholder:text-textSecondary/60 focus:border-accent focus:outline-none transition"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">Role</label>
                      <input
                        value={form.role}
                        onChange={update('role')}
                        placeholder="Head of Engineering"
                        className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white placeholder:text-textSecondary/60 focus:border-accent focus:outline-none transition"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">Team size</label>
                      <select
                        value={form.size}
                        onChange={update('size')}
                        className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white focus:border-accent focus:outline-none transition"
                      >
                        <option>1-10</option>
                        <option>10-50</option>
                        <option>50-250</option>
                        <option>250-1000</option>
                        <option>1000+</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">Interested in</label>
                      <select
                        value={form.interest}
                        onChange={update('interest')}
                        className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white focus:border-accent focus:outline-none transition"
                      >
                        <option>Pro plan</option>
                        <option>Enterprise plan</option>
                        <option>Custom integrations</option>
                        <option>Partnership</option>
                        <option>Something else</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold tracking-wider text-textSecondary uppercase mb-2">What are you trying to build?</label>
                    <textarea
                      rows={4}
                      value={form.message}
                      onChange={update('message')}
                      placeholder="Tell us about your integration challenges, the systems involved, and any compliance requirements…"
                      className="w-full px-4 py-2.5 rounded-lg bg-background border border-borderc text-white placeholder:text-textSecondary/60 focus:border-accent focus:outline-none transition resize-none"
                    ></textarea>
                  </div>

                  <label className="flex items-start gap-3 text-xs text-textSecondary">
                    <input type="checkbox" defaultChecked className="mt-0.5 accent-accent" />
                    <span>I agree to be contacted by Nexus about my inquiry, per the <a href="#" className="text-accent hover:underline">privacy policy</a>.</span>
                  </label>

                  <button
                    type="submit"
                    className="w-full py-3.5 rounded-xl font-semibold text-slate-900 bg-gradient-to-r from-accent to-accentWarm hover:brightness-110 shadow-lg shadow-accent/30 transition"
                  >
                    Send message →
                  </button>

                  <p className="text-center text-xs text-textSecondary">
                    Prefer email? <span className="text-accent">sales@nexus.io</span>
                  </p>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
