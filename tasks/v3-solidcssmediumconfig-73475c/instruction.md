# Website Design Replication Task

You are a Claude Code agent running inside a container. Your goal is to **replicate a multi-page website design as faithfully as possible** using **Solid JS and Vanilla CSS** via Vite.

## Step 1 — View the Reference Assets

Read each of the following files to see the target design. Use the `Read` tool on each path:

- `/app/assets/page_home_desktop.png` — Home (desktop)
- `/app/assets/page_work_desktop.png` — Work (desktop)
- `/app/assets/page_services_desktop.png` — Services (desktop)
- `/app/assets/page_about_desktop.png` — About (desktop)
- `/app/assets/page_contact_desktop.png` — Contact (desktop)

Study each asset carefully before writing any code. Note the color palette, typography, layout structure, spacing, and UI components on each page.

## Step 2 — Design Information

**Viewport width**: 1280px CSS pixels (set this as your rendering target)

**Reference page heights** (CSS pixels at 1280px wide):
- `index.html`: 2919px
- `index.html`: 2595px
- `index.html`: 2479px
- `index.html`: 3395px
- `index.html`: 1832px

**Fonts used in this design**:
- DM Sans
- system-ui
- sans-serif
(Embed these as web-safe fallbacks or system fonts — no external CDN/Google Fonts links)

**Color palette**:
- `background`: `#1a1a1a`
- `surface`: `#242424`
- `border`: `#3a3a3a`
- `primary`: `#f5f5f5`
- `accent`: `#ff6b35`
- `accent_cool`: `#667eea`
- `text_primary`: `#f0f0f0`
- `text_secondary`: `#999999`
- `cta`: `#ff6b35`

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
        ├── Work.jsx  (Work)
        ├── Services.jsx  (Services)
        ├── About.jsx  (About)
        ├── Contact.jsx  (Contact)
```

### Requirements

1. **Scaffold a Vite SOLID CSS project** in `/app/output/`.
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