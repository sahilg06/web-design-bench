# Website Design Replication Task

You are a Claude Code agent running inside a container. Your goal is to **replicate a multi-page website design as faithfully as possible** using **HTML and CSS only** — no JavaScript.

## Step 1 — View the Reference Screenshots

Read each of the following image files to see the target design. Use the `Read` tool on each path:

- `/app/assets/page_home_desktop.png` — Home (desktop)
- `/app/assets/page_collection_desktop.png` — Collection (desktop)
- `/app/assets/page_atelier_desktop.png` — Atelier (desktop)
- `/app/assets/page_journal_desktop.png` — Journal (desktop)
- `/app/assets/page_contact_desktop.png` — Contact (desktop)

Study each screenshot carefully before writing any code. Note the color palette, typography, layout structure, spacing, and UI components on each page.

## Step 2 — Design Information

**Viewport width**: 1280px CSS pixels (set this as your rendering target)

**Reference page heights** (CSS pixels at 1280px wide):
- `index.html`: 6058px
- `collection.html`: 4657px
- `atelier.html`: 5816px
- `journal.html`: 5225px
- `contact.html`: 2926px

**Fonts used in this design**:
- Playfair Display
- Georgia
- serif
(Embed these as web-safe fallbacks or system fonts — no external CDN/Google Fonts links)

**Color palette**:
- `background`: `#faf8f5`
- `surface`: `#f0ede8`
- `border`: `#d4cfc7`
- `primary`: `#1a1a1a`
- `accent`: `#c4a265`
- `text_primary`: `#1a1a1a`
- `text_secondary`: `#6b6560`
- `cta`: `#1a1a1a`

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
├── collection.html  (Collection)
├── atelier.html  (Atelier)
├── journal.html  (Journal)
├── contact.html  (Contact)
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