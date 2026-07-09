# Website Design Replication Task

You are a Claude Code agent running inside a container. Your goal is to **replicate a multi-page website design as faithfully as possible** using **React JS and Vanilla CSS** via Vite.

## Step 1 — View the Reference Assets

Read each of the following files to see the target design. Use the `Read` tool on each path:

- `/app/assets/page_home_desktop.png` — Home (desktop)
- `/app/assets/page_features_desktop.png` — Features (desktop)
- `/app/assets/page_pricing_desktop.png` — Pricing (desktop)
- `/app/assets/page_about_desktop.png` — About (desktop)
- `/app/assets/page_contact_desktop.png` — Contact (desktop)

Study each asset carefully before writing any code. Note the color palette, typography, layout structure, spacing, and UI components on each page.

## Step 2 — Design Information

**Viewport width**: 1280px CSS pixels (set this as your rendering target)

**Reference page heights** (CSS pixels at 1280px wide):
- `index.html`: 2352px
- `index.html`: 1407px
- `index.html`: 2073px
- `index.html`: 2269px
- `index.html`: 1672px

**Fonts used in this design**:
- Inter
- system-ui
- sans-serif
(Embed these as web-safe fallbacks or system fonts — no external CDN/Google Fonts links)

**Color palette**:
- `background`: `#f8fafc`
- `surface`: `#ffffff`
- `border`: `#e2e8f0`
- `primary`: `#0f172a`
- `accent`: `#2563eb`
- `text_primary`: `#1e293b`
- `text_secondary`: `#64748b`
- `cta`: `#2563eb`

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
├── index.html
└── src/
    ├── App.jsx
    ├── index.css
    └── pages/
        ├── Home.jsx  (Home)
        ├── Features.jsx  (Features)
        ├── Pricing.jsx  (Pricing)
        ├── About.jsx  (About)
        ├── Contact.jsx  (Contact)
```

### Requirements

1. **Scaffold a Vite REACT CSS project** in `/app/output/`.
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