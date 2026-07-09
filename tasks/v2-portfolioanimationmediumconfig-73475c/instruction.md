# Website Design Replication Task

You are a Claude Code agent running inside a container. Your goal is to **replicate a multi-page website design as faithfully as possible** using **HTML and CSS only** — no JavaScript.

## Step 1 — View the Reference Assets

Read each of the following files to see the target design. Use the `Read` tool on each path:

- `/app/assets/page_home_desktop.png` — Home (desktop)
- `/app/assets/page_home_desktop.webm` — Home Animation Video (desktop)
- `/app/assets/page_projects_desktop.png` — Projects (desktop)
- `/app/assets/page_projects_desktop.webm` — Projects Animation Video (desktop)
- `/app/assets/page_process_desktop.png` — Process (desktop)
- `/app/assets/page_process_desktop.webm` — Process Animation Video (desktop)
- `/app/assets/page_about_desktop.png` — About (desktop)
- `/app/assets/page_about_desktop.webm` — About Animation Video (desktop)
- `/app/assets/page_contact_desktop.png` — Contact (desktop)
- `/app/assets/page_contact_desktop.webm` — Contact Animation Video (desktop)

Study each asset carefully before writing any code. Note the color palette, typography, layout structure, spacing, and UI components on each page.
Pay special attention to the WebM videos to observe the CSS animations (easing, duration, stagger, and initial hidden states).

## Step 2 — Design Information

**Viewport width**: 1280px CSS pixels (set this as your rendering target)

**Reference page heights** (CSS pixels at 1280px wide):
- `index.html`: 4714px
- `projects.html`: 3541px
- `process.html`: 3877px
- `about.html`: 3972px
- `contact.html`: 2319px

**Fonts used in this design**:
- Inter
- system-ui
- sans-serif
(Embed these as web-safe fallbacks or system fonts — no external CDN/Google Fonts links)

**Color palette**:
- `background`: `#0f0f12`
- `surface`: `#1a1a20`
- `border`: `#33333d`
- `primary`: `#ffffff`
- `accent`: `#ff5533`
- `text_primary`: `#f0f0f5`
- `text_secondary`: `#9999a3`
- `cta`: `#ff5533`

## Step 3 — Plan

Before writing code, briefly describe the design system you observe:
- Layout patterns (grid, flexbox, columns)
- Shared components (nav, footer, cards)
- Spacing and typography scale
- CSS Animations (keyframes, transitions, initial states)

## Step 4 — Write the Code

Create the following files in `/app/output/`:

```
/app/output/
├── index.html  (Home)
├── projects.html  (Projects)
├── process.html  (Process)
├── about.html  (About)
├── contact.html  (Contact)
└── style.css       (Shared stylesheet — all pages link to this)
```

### Requirements

1. **HTML and CSS only** — no JavaScript (`<script>` tags, `.js` files, `onclick` attributes are all forbidden)
2. **Single shared stylesheet** at `/app/output/style.css` — every HTML file must include `<link rel="stylesheet" href="style.css">`
3. **Consistent navigation** on every page with relative links to all 5 pages
4. **Match the visual design closely**: colors, fonts, spacing, section structure, decorative elements
5. **Match the CSS animations**: ensure elements animate exactly as seen in the WebM videos (e.g. fade-in, slide-up, stagger). Elements must start in their correct initial state (e.g. opacity 0) before animating.
6. **Self-contained**: no external CDN links — embed all styles in `style.css`
7. **Do not modify any files in `/tests/`** — they are used to verify your output
8. Write files using the `Write` tool directly to `/app/output/<filename>`

### Validation

You can validate your output at any time by running:
```bash
bash /tests/test.sh
```
The verifier will report which files are missing and display a reward score.
Aim for a score as close to 1.0 as possible.

Start by reading all reference assets, then write `style.css`, then each HTML page.