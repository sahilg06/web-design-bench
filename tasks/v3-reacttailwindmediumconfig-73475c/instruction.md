# Website Design Replication Task

You are a Claude Code agent running inside a container. Your goal is to **replicate a multi-page website design as faithfully as possible** using **React JS and Tailwind CSS** via Vite.

## Step 1 — View the Reference Assets

Read each of the following files to see the target design. Use the `Read` tool on each path:

- `/app/assets/page_home_desktop.png` — Home (desktop)
- `/app/assets/page_solutions_desktop.png` — Solutions (desktop)
- `/app/assets/page_pricing_desktop.png` — Pricing (desktop)
- `/app/assets/page_docs_desktop.png` — Docs (desktop)
- `/app/assets/page_contact_desktop.png` — Contact (desktop)

Study each asset carefully before writing any code. Note the color palette, typography, layout structure, spacing, and UI components on each page.

## Step 2 — Design Information

**Viewport width**: 1280px CSS pixels (set this as your rendering target)

**Reference page heights** (CSS pixels at 1280px wide):
- `index.html`: 3933px
- `index.html`: 3224px
- `index.html`: 3133px
- `index.html`: 3029px
- `index.html`: 1729px

**Fonts used in this design**:
- Roboto
- system-ui
- sans-serif
(Embed these as web-safe fallbacks or system fonts — no external CDN/Google Fonts links)

**Color palette**:
- `background`: `#0f172a`
- `surface`: `#1e293b`
- `border`: `#334155`
- `primary`: `#ffffff`
- `accent`: `#38bdf8`
- `accent_warm`: `#818cf8`
- `text_primary`: `#f1f5f9`
- `text_secondary`: `#94a3b8`
- `cta`: `#38bdf8`

## Step 3 — Plan

Before writing code, briefly describe the design system you observe:
- Layout patterns (grid, flexbox, columns)
- Shared components (nav, footer, cards)
- Spacing and typography scale

## Step 4 — Write the Code

Create the following files in `/app/output/`:

```
/app/output/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── index.html
└── src/
    ├── App.jsx
    ├── index.css
    └── pages/
        ├── Home.jsx  (Home)
        ├── Solutions.jsx  (Solutions)
        ├── Pricing.jsx  (Pricing)
        ├── Docs.jsx  (Docs)
        ├── Contact.jsx  (Contact)
```

### Requirements

1. **Scaffold a Vite REACT TAILWIND project** in `/app/output/`.
2. **`vite.config.js` MUST include `base: './'`** so the app builds with relative file paths.
3. **Consistent navigation** in `src/App.jsx` to switch between all page components.
4. **Match the visual design closely**: colors, fonts, spacing, section structure, decorative elements.
6. **Self-contained**: no external CDN links — embed all styles/configs locally.
7. **Do not modify any files in `/tests/`** — they are used to verify your output.
8. Write files using the `Write` tool directly to `/app/output/<filename>`.

### Validation

You can validate your output at any time by running:
```bash
bash /tests/test.sh
```
The verifier will report which files are missing and display a reward score.
Aim for a score as close to 1.0 as possible.

Start by reading all reference assets, then write your configuration/styles, then each component/page.