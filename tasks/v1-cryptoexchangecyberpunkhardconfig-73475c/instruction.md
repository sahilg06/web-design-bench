# Website Design Replication Task

You are a Claude Code agent running inside a container. Your goal is to **replicate a multi-page website design as faithfully as possible** using **HTML and CSS only** — no JavaScript.

## Step 1 — View the Reference Screenshots

Read each of the following image files to see the target design. Use the `Read` tool on each path:

- `/app/assets/page_home_desktop.png` — Home (desktop)
- `/app/assets/page_markets_desktop.png` — Markets (desktop)
- `/app/assets/page_security_desktop.png` — Security (desktop)
- `/app/assets/page_fees_desktop.png` — Fees (desktop)
- `/app/assets/page_contact_desktop.png` — Support (desktop)

Study each screenshot carefully before writing any code. Note the color palette, typography, layout structure, spacing, and UI components on each page.

## Step 2 — Design Information

**Viewport width**: 1280px CSS pixels (set this as your rendering target)

**Reference page heights** (CSS pixels at 1280px wide):
- `index.html`: 3755px
- `markets.html`: 2937px
- `security.html`: 4660px
- `fees.html`: 4088px
- `contact.html`: 4907px

**Fonts used in this design**:
- JetBrains Mono
- Fira Code
- monospace
(Embed these as web-safe fallbacks or system fonts — no external CDN/Google Fonts links)

**Color palette**:
- `background`: `#0a0a0a`
- `surface`: `#111111`
- `border`: `#1e1e1e`
- `primary`: `#00ff88`
- `accent`: `#ff006e`
- `text_primary`: `#e0e0e0`
- `text_secondary`: `#666666`
- `cta`: `#00ff88`

## Step 3 — Plan

Before writing code, briefly describe the design system you observe:
- Layout patterns (grid, flexbox, columns)
- Shared components (nav, footer, cards)
- Spacing and typography scale

## Step 4 — Write the Code

Create the following files in `/app/output/`:

```
/app/output/
├── index.html  (Home)
├── markets.html  (Markets)
├── security.html  (Security)
├── fees.html  (Fees)
├── contact.html  (Support)
└── style.css       (Shared stylesheet — all pages link to this)
```

### Requirements

1. **HTML and CSS only** — no JavaScript (`<script>` tags, `.js` files, `onclick` attributes are all forbidden)
2. **Single shared stylesheet** at `/app/output/style.css` — every HTML file must include `<link rel="stylesheet" href="style.css">`
3. **Consistent navigation** on every page with relative links to all 5 pages
4. **Match the visual design closely**: colors, fonts, spacing, section structure, decorative elements
5. **Self-contained**: no external CDN links — embed all styles in `style.css`
6. **Do not modify any files in `/tests/`** — they are used to verify your output
7. Write files using the `Write` tool directly to `/app/output/<filename>`

### Validation

You can validate your output at any time by running:
```bash
bash /tests/test.sh
```
The verifier will report which files are missing and display a reward score.
Aim for a score as close to 1.0 as possible.

Start by reading all reference screenshots, then write `style.css`, then each HTML page.