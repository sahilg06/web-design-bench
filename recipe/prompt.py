"""
Prompt renderer for the website generation agent.

Produces (system_prompt, user_prompt) that Claude uses to generate a complete,
production-quality multi-page website from a DesignSpec across various frameworks:
  - html_css       : Pure HTML + Vanilla CSS (No JS)
  - react_css      : React JS + Vanilla CSS (Vite scaffolding)
  - react_tailwind : React JS + Tailwind CSS (Vite scaffolding)
  - solid_css      : Solid JS + Vanilla CSS (Vite scaffolding)
  - solid_tailwind : Solid JS + Tailwind CSS (Vite scaffolding)

Design philosophy:
  - The system prompt establishes an expert web designer identity with framework rules.
  - The user prompt provides a full design brief: brand, colors, typography,
    per-page content guidance, and quality requirements.
  - XML file tags (<file name="...">...</file>) delimit each output file.
"""

from __future__ import annotations

# ── System Prompts ───────────────────────────────────────────────────────────

SYSTEM_PROMPT_HTML_CSS = """\
You are an expert web designer and senior frontend developer. You produce beautiful,
professional, pixel-perfect websites for real brands.

ABSOLUTE RULES — violating any rule makes the output unusable:
1. HTML + CSS ONLY. Zero JavaScript. No <script> tags. No on* attributes. No .js files.
2. ALL styles go in style.css. HTML files contain ZERO <style> tags.
3. Every HTML file MUST contain: <link rel="stylesheet" href="style.css">
4. Every HTML file MUST contain a <nav> with links to ALL pages.
5. Output each file using exactly this XML wrapper:
   <file name="filename.ext">
   ...complete file content...
   </file>
6. File names must match exactly what is requested.
7. Do NOT truncate output. Complete every file fully.
8. Use semantic HTML5 elements: <header>, <main>, <section>, <article>, <footer>.
9. Use real, specific content for the brand — no "Lorem ipsum" or placeholder text.
10. All image placeholders must use CSS-styled <div> elements with background-color,
    NOT <img> tags with broken src attributes.
"""

SYSTEM_PROMPT_REACT_CSS = """\
You are an expert web designer and senior React frontend developer. You produce beautiful,
professional, pixel-perfect React websites for real brands using Vite and Vanilla CSS.

ABSOLUTE RULES — violating any rule makes the output unusable:
1. You are building a React Single Page Application (SPA) using Vite.
2. ALL custom styles go in src/index.css using Vanilla CSS.
3. Output each file using exactly this XML wrapper:
   <file name="filename.ext">
   ...complete file content...
   </file>
4. File names must match exactly what is requested (including package.json, vite.config.js, etc.).
5. Do NOT truncate output. Complete every file fully.
6. Use semantic HTML5 elements in JSX: <header>, <main>, <section>, <article>, <footer>.
7. Use real, specific content for the brand — no "Lorem ipsum" or placeholder text.
8. All image placeholders must use CSS-styled <div> elements with background-color.
9. Implement simple in-memory tab/page navigation in src/App.jsx so the user can switch between all pages.
"""

SYSTEM_PROMPT_REACT_TAILWIND = """\
You are an expert web designer and senior React frontend developer. You produce beautiful,
professional, pixel-perfect React websites for real brands using Vite and Tailwind CSS.

ABSOLUTE RULES — violating any rule makes the output unusable:
1. You are building a React Single Page Application (SPA) using Vite and Tailwind CSS.
2. Use Tailwind CSS utility classes (className="bg-slate-900 text-white...") for all styling.
3. Output each file using exactly this XML wrapper:
   <file name="filename.ext">
   ...complete file content...
   </file>
4. File names must match exactly what is requested (including package.json, vite.config.js, tailwind.config.js, etc.).
5. Do NOT truncate output. Complete every file fully.
6. Use semantic HTML5 elements in JSX: <header>, <main>, <section>, <article>, <footer>.
7. Use real, specific content for the brand — no "Lorem ipsum" or placeholder text.
8. All image placeholders must use Tailwind-styled <div> elements with background-color.
9. Implement simple in-memory tab/page navigation in src/App.jsx so the user can switch between all pages.
"""

SYSTEM_PROMPT_SOLID_TAILWIND = """\
You are an expert web designer and senior Solid JS frontend developer. You produce beautiful,
professional, pixel-perfect Solid JS websites for real brands using Vite and Tailwind CSS.

ABSOLUTE RULES — violating any rule makes the output unusable:
1. You are building a Solid JS Single Page Application (SPA) using Vite and Tailwind CSS.
2. Use Tailwind CSS utility classes (class="bg-slate-900 text-white...") for all styling. Note: Solid JS uses `class`, NOT `className`.
3. Output each file using exactly this XML wrapper:
   <file name="filename.ext">
   ...complete file content...
   </file>
4. File names must match exactly what is requested (including package.json, vite.config.js, tailwind.config.js, etc.).
5. Do NOT truncate output. Complete every file fully.
6. Use semantic HTML5 elements in JSX: <header>, <main>, <section>, <article>, <footer>.
7. Use real, specific content for the brand — no "Lorem ipsum" or placeholder text.
8. All image placeholders must use Tailwind-styled <div> elements with background-color.
9. Implement simple in-memory tab/page navigation in src/App.jsx using Solid signals (`createSignal`) so the user can switch between all pages.
"""

SYSTEM_PROMPT_SOLID_CSS = """\
You are an expert web designer and senior Solid JS frontend developer. You produce beautiful,
professional, pixel-perfect Solid JS websites for real brands using Vite and Vanilla CSS.

ABSOLUTE RULES — violating any rule makes the output unusable:
1. You are building a Solid JS Single Page Application (SPA) using Vite.
2. ALL custom styles go in src/index.css using Vanilla CSS.
3. Output each file using exactly this XML wrapper:
   <file name="filename.ext">
   ...complete file content...
   </file>
4. File names must match exactly what is requested (including package.json, vite.config.js, etc.).
5. Do NOT truncate output. Complete every file fully.
6. Use semantic HTML5 elements in JSX: <header>, <main>, <section>, <article>, <footer>.
7. Use real, specific content for the brand — no "Lorem ipsum" or placeholder text.
8. All image placeholders must use CSS-styled <div> elements with background-color.
9. Implement simple in-memory tab/page navigation in src/App.jsx using Solid signals (`createSignal`) so the user can switch between all pages.
10. Note: Solid JS uses `class`, NOT `className` for JSX styling.
"""


# ── User Prompt Builders ─────────────────────────────────────────────────────

def build_user_prompt_html_css(spec: dict) -> str:
    brand      = spec["brand_name"]
    tagline    = spec["brand_tagline"]
    archetype  = spec["archetype"]
    style      = spec["visual_style"]
    directives = spec["design_directives"]
    pages      = spec["pages"]
    colors     = spec["colors"]
    fonts      = spec["fonts"]
    difficulty = spec["difficulty"]

    colors_block = "\n".join(f"  {k}: {v}" for k, v in colors.items())
    fonts_str = " / ".join(fonts) if fonts else "system-ui, sans-serif"
    nav_links = "  ".join(f'<a href="{p["file"]}">{p["label"]}</a>' for p in pages)

    pages_block = ""
    for i, p in enumerate(pages, 1):
        pages_block += (
            f"\n  {i}. {p['file']} — {p['label']}\n"
            f"     Content guide: {p['description']}\n"
        )

    filenames_listed = "\n".join(f"  - {p['file']}" for p in pages)
    css_min_lines = {"easy": 200, "medium": 300, "hard": 400}.get(difficulty, 250)

    return f"""\
Create a complete, professional {len(pages)}-page website for **{brand}** — _{tagline}_.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND & DESIGN BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype : {archetype}
Style     : {style}
Difficulty: {difficulty}
Directives: {directives}

COLOR PALETTE — define every color as a CSS custom property on :root:
{colors_block}

TYPOGRAPHY:
  Fonts: {fonts_str}
  Use system font stacks only — no external CDN or Google Fonts <link> tags.
  Define font-family in CSS using these names as the preferred stack.

NAVIGATION (identical on every page):
  {nav_links}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGES TO CREATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pages_block}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
style.css REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Write AT LEAST {css_min_lines} lines of CSS. Must include:
  ✓ :root block with ALL color and spacing variables
  ✓ CSS reset (margin/padding 0, box-sizing border-box)
  ✓ Base typography scale and body styles
  ✓ Navigation / header component
  ✓ Hero / banner section styles
  ✓ Card component styles
  ✓ Button styles (primary + secondary)
  ✓ Form element styles (inputs, textareas, selects, labels)
  ✓ Grid and layout utility classes
  ✓ Table styles (if the design includes tables)
  ✓ Footer styles
  ✓ At least one responsive media query (max-width: 768px)
  ✓ Image placeholder styles (colored divs with aspect ratios)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HTML REQUIREMENTS (every page)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ <!DOCTYPE html><html lang="en">
  ✓ <meta charset="UTF-8"><meta name="viewport" content="...">
  ✓ <title> tag with brand name and page name
  ✓ <link rel="stylesheet" href="style.css">  ← REQUIRED
  ✓ <header> with <nav> containing links to all {len(pages)} pages
  ✓ <main> with multiple <section> elements matching the content guide
  ✓ Real, specific content for {brand} (no "Lorem ipsum", no "Company Name")
  ✓ <footer> with copyright and links
  ✓ Use image placeholders as <div> with class and background-color, not <img>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Output all {len(pages) + 1} files in order:
  - style.css
{filenames_listed}

Use the format:
<file name="style.css">
/* complete CSS */
</file>
<file name="{pages[0]['file']}">
<!-- complete HTML -->
</file>
... and so on for all files. Do not stop until all files are complete.
"""


def build_user_prompt_react_css(spec: dict) -> str:
    brand      = spec["brand_name"]
    tagline    = spec["brand_tagline"]
    archetype  = spec["archetype"]
    style      = spec["visual_style"]
    directives = spec["design_directives"]
    pages      = spec["pages"]
    colors     = spec["colors"]
    fonts      = spec["fonts"]

    colors_block = "\n".join(f"  {k}: {v}" for k, v in colors.items())
    fonts_str = " / ".join(fonts) if fonts else "system-ui, sans-serif"

    pages_block = ""
    page_imports = []
    page_files = []
    for i, p in enumerate(pages, 1):
        comp_name = p["name"].replace("page_", "").capitalize()
        filename = f"src/pages/{comp_name}.jsx"
        page_imports.append(f"import {comp_name} from './pages/{comp_name}';")
        page_files.append(filename)
        pages_block += (
            f"\n  {i}. {filename} — {p['label']}\n"
            f"     Content guide: {p['description']}\n"
        )

    filenames_listed = "\n".join(f"  - {f}" for f in page_files)

    return f"""\
Create a complete, professional React Single Page Application (SPA) for **{brand}** — _{tagline}_ using Vite and Vanilla CSS.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND & DESIGN BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype : {archetype}
Style     : {style}
Directives: {directives}

COLOR PALETTE — define every color as a CSS custom property in src/index.css:
{colors_block}

TYPOGRAPHY:
  Fonts: {fonts_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGES TO CREATE (as React Components)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pages_block}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Scaffold a Vite React project. You must provide:
   - package.json (include react, react-dom, vite, @vitejs/plugin-react)
   - vite.config.js (MUST include `base: './'` so it builds with relative paths)
   - index.html (with <div id="root"></div> and <script type="module" src="/src/main.jsx"></script>)
   - src/main.jsx (renders <App /> into #root)
   - src/App.jsx (main layout containing <nav> and <footer>, with state `const [activeTab, setActiveTab] = useState('{pages[0]['name']}');` to switch between page components)
   - src/index.css (Vanilla CSS with all custom properties, resets, and component styles)

2. Navigation in src/App.jsx:
   - The <nav> bar must contain buttons/links for all {len(pages)} pages.
   - Clicking a nav item must update `activeTab` so the corresponding page component renders in <main>.
   - Ensure active tab styling is clearly visible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Output all required files in order:
  - package.json
  - vite.config.js
  - index.html
  - src/main.jsx
  - src/index.css
  - src/App.jsx
{filenames_listed}

Use the format:
<file name="package.json">
{{
  "name": "{brand.lower().replace(' ', '-')}",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.3.0",
    "vite": "^5.2.11"
  }}
}}
</file>
<file name="vite.config.js">
import {{ defineConfig }} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({{
  plugins: [react()],
  base: './',
}});
</file>
... and so on for all files. Do not stop until all files are complete.
"""


def build_user_prompt_react_tailwind(spec: dict) -> str:
    brand      = spec["brand_name"]
    tagline    = spec["brand_tagline"]
    archetype  = spec["archetype"]
    style      = spec["visual_style"]
    directives = spec["design_directives"]
    pages      = spec["pages"]
    colors     = spec["colors"]
    fonts      = spec["fonts"]

    colors_block = "\n".join(f"  {k}: {v}" for k, v in colors.items())
    fonts_str = " / ".join(fonts) if fonts else "system-ui, sans-serif"

    pages_block = ""
    page_files = []
    for i, p in enumerate(pages, 1):
        comp_name = p["name"].replace("page_", "").capitalize()
        filename = f"src/pages/{comp_name}.jsx"
        page_files.append(filename)
        pages_block += (
            f"\n  {i}. {filename} — {p['label']}\n"
            f"     Content guide: {p['description']}\n"
        )

    filenames_listed = "\n".join(f"  - {f}" for f in page_files)

    return f"""\
Create a complete, professional React Single Page Application (SPA) for **{brand}** — _{tagline}_ using Vite and Tailwind CSS.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND & DESIGN BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype : {archetype}
Style     : {style}
Directives: {directives}

COLOR PALETTE — extend these colors in tailwind.config.js:
{colors_block}

TYPOGRAPHY:
  Fonts: {fonts_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGES TO CREATE (as React Components)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pages_block}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Scaffold a Vite React + Tailwind CSS project. You must provide:
   - package.json (include react, react-dom, vite, @vitejs/plugin-react, tailwindcss, postcss, autoprefixer)
   - vite.config.js (MUST include `base: './'` so it builds with relative paths)
   - tailwind.config.js (configure `content: ['./index.html', './src/**/*.{{js,ts,jsx,tsx}}']` and extend theme colors)
   - postcss.config.js (configure tailwindcss and autoprefixer plugins)
   - index.html (with <div id="root"></div> and <script type="module" src="/src/main.jsx"></script>)
   - src/main.jsx (renders <App /> into #root)
   - src/index.css (MUST include `@tailwind base; @tailwind components; @tailwind utilities;`)
   - src/App.jsx (main layout containing <nav> and <footer>, with state `const [activeTab, setActiveTab] = useState('{pages[0]['name']}');` to switch between page components)

2. Navigation in src/App.jsx:
   - The <nav> bar must contain buttons/links for all {len(pages)} pages.
   - Clicking a nav item must update `activeTab` so the corresponding page component renders in <main>.
   - Ensure active tab styling is clearly visible using Tailwind classes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Output all required files in order:
  - package.json
  - vite.config.js
  - tailwind.config.js
  - postcss.config.js
  - index.html
  - src/main.jsx
  - src/index.css
  - src/App.jsx
{filenames_listed}

Use the format:
<file name="package.json">
{{
  "name": "{brand.lower().replace(' ', '-')}",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "vite": "^5.2.11"
  }}
}}
</file>
<file name="vite.config.js">
import {{ defineConfig }} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({{
  plugins: [react()],
  base: './',
}});
</file>
<file name="tailwind.config.js">
/** @type {{import('tailwindcss').Config}} */
export default {{
  content: [
    "./index.html",
    "./src/**/*.{{js,ts,jsx,tsx}}",
  ],
  theme: {{
    extend: {{
      colors: {{
        primary: "{colors.get('primary', '#ffffff')}",
        accent: "{colors.get('accent', '#3b82f6')}",
        background: "{colors.get('background', '#0f172a')}",
        surface: "{colors.get('surface', '#1e293b')}",
      }},
    }},
  }},
  plugins: [],
}}
</file>
<file name="postcss.config.js">
export default {{
  plugins: {{
    tailwindcss: {{}},
    autoprefixer: {{}},
  }},
}}
</file>
... and so on for all files. Do not stop until all files are complete.
"""


def build_user_prompt_solid_css(spec: dict) -> str:
    brand      = spec["brand_name"]
    tagline    = spec["brand_tagline"]
    archetype  = spec["archetype"]
    style      = spec["visual_style"]
    directives = spec["design_directives"]
    pages      = spec["pages"]
    colors     = spec["colors"]
    fonts      = spec["fonts"]

    colors_block = "\n".join(f"  {k}: {v}" for k, v in colors.items())
    fonts_str = " / ".join(fonts) if fonts else "system-ui, sans-serif"

    pages_block = ""
    page_files = []
    for i, p in enumerate(pages, 1):
        comp_name = p["name"].replace("page_", "").capitalize()
        filename = f"src/pages/{comp_name}.jsx"
        page_files.append(filename)
        pages_block += (
            f"\n  {i}. {filename} — {p['label']}\n"
            f"     Content guide: {p['description']}\n"
        )

    filenames_listed = "\n".join(f"  - {f}" for f in page_files)

    return f"""\
Create a complete, professional Solid JS Single Page Application (SPA) for **{brand}** — _{tagline}_ using Vite and Vanilla CSS.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND & DESIGN BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype : {archetype}
Style     : {style}
Directives: {directives}

COLOR PALETTE — define every color as a CSS custom property in src/index.css:
{colors_block}

TYPOGRAPHY:
  Fonts: {fonts_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGES TO CREATE (as Solid JS Components)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pages_block}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Scaffold a Vite Solid JS project. You must provide:
   - package.json (include solid-js, vite, vite-plugin-solid)
   - vite.config.js (MUST include `base: './'` and vite-plugin-solid)
   - index.html (with <div id="root"></div> and <script type="module" src="/src/index.jsx"></script>)
   - src/index.jsx (renders <App /> into #root using `render(() => <App />, document.getElementById('root'))`)
   - src/index.css (Vanilla CSS with all custom properties, resets, and component styles)
   - src/App.jsx (main layout containing <nav> and <footer>, with Solid signal `const [activeTab, setActiveTab] = createSignal('{pages[0]['name']}');` to switch between page components)

2. Solid JS Specifics:
   - Use `class`, NOT `className` for JSX styling.
   - Use `{{activeTab() === 'page_home' && <Home />}}` or Solid's `<Match>` / `<Switch>` for tab switching.
   - Remember that signals are functions: use `activeTab()` to read and `setActiveTab('page_name')` to write.

3. Navigation in src/App.jsx:
   - The <nav> bar must contain buttons/links for all {len(pages)} pages.
   - Clicking a nav item must update `activeTab` so the corresponding page component renders in <main>.
   - Ensure active tab styling is clearly visible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Output all required files in order:
  - package.json
  - vite.config.js
  - index.html
  - src/index.jsx
  - src/index.css
  - src/App.jsx
{filenames_listed}

Use the format:
<file name="package.json">
{{
  "name": "{brand.lower().replace(' ', '-')}",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "solid-js": "^1.8.17"
  }},
  "devDependencies": {{
    "vite": "^5.2.11",
    "vite-plugin-solid": "^2.10.2"
  }}
}}
</file>
<file name="vite.config.js">
import {{ defineConfig }} from 'vite';
import solidPlugin from 'vite-plugin-solid';

export default defineConfig({{
  plugins: [solidPlugin()],
  base: './',
}});
</file>
... and so on for all files. Do not stop until all files are complete.
"""


def build_user_prompt_solid_tailwind(spec: dict) -> str:
    brand      = spec["brand_name"]
    tagline    = spec["brand_tagline"]
    archetype  = spec["archetype"]
    style      = spec["visual_style"]
    directives = spec["design_directives"]
    pages      = spec["pages"]
    colors     = spec["colors"]
    fonts      = spec["fonts"]

    colors_block = "\n".join(f"  {k}: {v}" for k, v in colors.items())
    fonts_str = " / ".join(fonts) if fonts else "system-ui, sans-serif"

    pages_block = ""
    page_files = []
    for i, p in enumerate(pages, 1):
        comp_name = p["name"].replace("page_", "").capitalize()
        filename = f"src/pages/{comp_name}.jsx"
        page_files.append(filename)
        pages_block += (
            f"\n  {i}. {filename} — {p['label']}\n"
            f"     Content guide: {p['description']}\n"
        )

    filenames_listed = "\n".join(f"  - {f}" for f in page_files)

    return f"""\
Create a complete, professional Solid JS Single Page Application (SPA) for **{brand}** — _{tagline}_ using Vite and Tailwind CSS.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND & DESIGN BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype : {archetype}
Style     : {style}
Directives: {directives}

COLOR PALETTE — extend these colors in tailwind.config.js:
{colors_block}

TYPOGRAPHY:
  Fonts: {fonts_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGES TO CREATE (as Solid JS Components)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pages_block}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Scaffold a Vite Solid JS + Tailwind CSS project. You must provide:
   - package.json (include solid-js, vite, vite-plugin-solid, tailwindcss, postcss, autoprefixer)
   - vite.config.js (MUST include `base: './'` and vite-plugin-solid)
   - tailwind.config.js (configure `content: ['./index.html', './src/**/*.{{js,ts,jsx,tsx}}']` and extend theme colors)
   - postcss.config.js (configure tailwindcss and autoprefixer plugins)
   - index.html (with <div id="root"></div> and <script type="module" src="/src/index.jsx"></script>)
   - src/index.jsx (renders <App /> into #root using `render(() => <App />, document.getElementById('root'))`)
   - src/index.css (MUST include `@tailwind base; @tailwind components; @tailwind utilities;`)
   - src/App.jsx (main layout containing <nav> and <footer>, with Solid signal `const [activeTab, setActiveTab] = createSignal('{pages[0]['name']}');` to switch between page components)

2. Solid JS Specifics:
   - Use `class`, NOT `className` for JSX styling.
   - Use Solid's `<Match>` / `<Switch>` or simple function calling `{{activeTab() === 'page_home' && <Home />}}` for tab switching.
   - Remember that signals are functions: use `activeTab()` to read and `setActiveTab('page_name')` to write.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Output all required files in order:
  - package.json
  - vite.config.js
  - tailwind.config.js
  - postcss.config.js
  - index.html
  - src/index.jsx
  - src/index.css
  - src/App.jsx
{filenames_listed}

Use the format:
<file name="package.json">
{{
  "name": "{brand.lower().replace(' ', '-')}",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "solid-js": "^1.8.17"
  }},
  "devDependencies": {{
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "vite": "^5.2.11",
    "vite-plugin-solid": "^2.10.2"
  }}
}}
</file>
<file name="vite.config.js">
import {{ defineConfig }} from 'vite';
import solidPlugin from 'vite-plugin-solid';

export default defineConfig({{
  plugins: [solidPlugin()],
  base: './',
}});
</file>
<file name="tailwind.config.js">
/** @type {{import('tailwindcss').Config}} */
export default {{
  content: [
    "./index.html",
    "./src/**/*.{{js,ts,jsx,tsx}}",
  ],
  theme: {{
    extend: {{
      colors: {{
        primary: "{colors.get('primary', '#ffffff')}",
        accent: "{colors.get('accent', '#3b82f6')}",
        background: "{colors.get('background', '#0f172a')}",
        surface: "{colors.get('surface', '#1e293b')}",
      }},
    }},
  }},
  plugins: [],
}}
</file>
<file name="postcss.config.js">
export default {{
  plugins: {{
    tailwindcss: {{}},
    autoprefixer: {{}},
  }},
}}
</file>
... and so on for all files. Do not stop until all files are complete.
"""


def build_prompts(spec: dict) -> tuple[str, str]:
    """
    Build both system and user prompts from a DesignSpec based on the framework.

    Returns:
        Tuple of (system_prompt, user_prompt).
    """
    fw = spec.get("framework", "html_css")

    if fw == "react_css":
        return SYSTEM_PROMPT_REACT_CSS, build_user_prompt_react_css(spec)
    elif fw == "react_tailwind":
        return SYSTEM_PROMPT_REACT_TAILWIND, build_user_prompt_react_tailwind(spec)
    elif fw == "solid_css":
        return SYSTEM_PROMPT_SOLID_CSS, build_user_prompt_solid_css(spec)
    elif fw == "solid_tailwind":
        return SYSTEM_PROMPT_SOLID_TAILWIND, build_user_prompt_solid_tailwind(spec)
    else:
        return SYSTEM_PROMPT_HTML_CSS, build_user_prompt_html_css(spec)

