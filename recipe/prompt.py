"""
Prompt renderer for the HTML/CSS generation agent.

Produces (system_prompt, user_prompt) that Claude uses to generate a complete,
production-quality multi-page website from a DesignSpec.

Design philosophy:
  - The system prompt establishes an expert web designer identity with hard rules.
  - The user prompt provides a full design brief: brand, colors, typography,
    per-page content guidance, and quality requirements.
  - XML file tags (<file name="...">...</file>) delimit each output file.
  - All styles MUST go in style.css — no inline <style> tags allowed.

Output quality requirements encoded in the prompts:
  - Real, brand-specific content (no Lorem Ipsum)
  - Modern CSS: custom properties, flexbox, grid
  - Minimum 250 lines of CSS covering the full design system
  - Rich page structure: hero, multiple sections, footer on every page
"""

from __future__ import annotations

SYSTEM_PROMPT = """\
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


def build_user_prompt(spec: dict) -> str:
    """
    Render a DesignSpec into a detailed user prompt for Claude.

    The prompt includes brand info, color palette, font choices, page descriptions,
    layout directives, and strict quality requirements.

    Args:
        spec: A DesignSpec dictionary from spec.py.

    Returns:
        A formatted user prompt string ready to send to Claude.
    """
    brand      = spec["brand_name"]
    tagline    = spec["brand_tagline"]
    archetype  = spec["archetype"]
    style      = spec["visual_style"]
    directives = spec["design_directives"]
    pages      = spec["pages"]
    colors     = spec["colors"]
    fonts      = spec["fonts"]
    difficulty = spec["difficulty"]

    # ── Color palette block ──────────────────────────────────────────────
    colors_block = "\n".join(f"  {k}: {v}" for k, v in colors.items())

    # ── Font stack ───────────────────────────────────────────────────────
    fonts_str = " / ".join(fonts) if fonts else "system-ui, sans-serif"

    # ── Navigation links ─────────────────────────────────────────────────
    nav_links = "  ".join(
        f'<a href="{p["file"]}">{p["label"]}</a>' for p in pages
    )

    # ── Per-page content guides ──────────────────────────────────────────
    pages_block = ""
    for i, p in enumerate(pages, 1):
        pages_block += (
            f"\n  {i}. {p['file']} — {p['label']}\n"
            f"     Content guide: {p['description']}\n"
        )

    # ── File list ────────────────────────────────────────────────────────
    filenames_listed = "\n".join(f"  - {p['file']}" for p in pages)

    # ── Difficulty-specific CSS requirements ─────────────────────────────
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


def build_prompts(spec: dict) -> tuple[str, str]:
    """
    Build both system and user prompts from a DesignSpec.

    Returns:
        Tuple of (system_prompt, user_prompt).
    """
    return SYSTEM_PROMPT, build_user_prompt(spec)
