# Website Design Replication Task

You are a Claude Code agent running inside a container. Your goal is to **replicate a multi-page website design as faithfully as possible** using **Solid JS and Tailwind CSS** via Vite.

## Step 1 — View the Reference Assets

Read each of the following files to see the target design. Use the `Read` tool on each path:

- `/app/assets/page_home_desktop.png` — Home (desktop)
- `/app/assets/page_markets_desktop.png` — Markets (desktop)
- `/app/assets/page_trade_desktop.png` — Trade (desktop)
- `/app/assets/page_earn_desktop.png` — Earn (desktop)
- `/app/assets/page_wallet_desktop.png` — Wallet (desktop)

Study each asset carefully before writing any code. Note the color palette, typography, layout structure, spacing, and UI components on each page.

## Step 2 — Design Information

**Viewport width**: 1280px CSS pixels (set this as your rendering target)

**Reference page heights** (CSS pixels at 1280px wide):
- `index.html`: 2507px
- `index.html`: 1740px
- `index.html`: 1295px
- `index.html`: 1635px
- `index.html`: 1843px

**Fonts used in this design**:
- Outfit
- system-ui
- sans-serif
(Embed these as web-safe fallbacks or system fonts — no external CDN/Google Fonts links)

**Color palette**:
- `background`: `#09090b`
- `surface`: `#18181b`
- `border`: `#27272a`
- `primary`: `#ffffff`
- `accent`: `#10b981`
- `accent_warm`: `#f59e0b`
- `danger`: `#ef4444`
- `text_primary`: `#fafafa`
- `text_secondary`: `#a1a1aa`
- `cta`: `#10b981`

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
        ├── Markets.jsx  (Markets)
        ├── Trade.jsx  (Trade)
        ├── Earn.jsx  (Earn)
        ├── Wallet.jsx  (Wallet)
```

### Requirements

1. **Scaffold a Vite SOLID TAILWIND project** in `/app/output/`.
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