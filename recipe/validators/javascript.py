"""
JavaScript validator — hard rejection.

Scans all HTML files for any JavaScript presence:
  - <script> tags (inline or external)
  - on* event attributes (onclick, onload, onmouseover, etc.)
  - javascript: URIs in href/src/action attributes
  - .js file references in <script src> or <link href>

CSS files are also checked for embedded JS expressions (rare but possible
in legacy IE expressions).

Any violation is a hard reject — the generated site cannot be used as a task.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ── Compiled patterns ────────────────────────────────────────────────────────
_ON_ATTR_RE = re.compile(r"^on\w+$", re.IGNORECASE)
_JS_SRC_RE  = re.compile(r"\.js(\?.*)?$", re.IGNORECASE)
_CSS_EXPRESSION_RE = re.compile(r"expression\s*\(", re.IGNORECASE)


def validate_html_file(path: Path) -> list[str]:
    """
    Scan a single HTML file for JavaScript violations.

    Args:
        path: Path to the HTML file.

    Returns:
        List of violation description strings. Empty = clean.
    """
    violations: list[str] = []

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        violations.append(f"{path.name}: cannot read file — {e}")
        return violations

    soup = BeautifulSoup(text, "html.parser")

    for tag in soup.find_all(True):
        # Check for <script> tags
        if tag.name == "script":
            violations.append(f"{path.name}: <script> tag found")

        # Check all attributes
        for attr, value in tag.attrs.items():
            # Normalize list-type attribute values
            if isinstance(value, list):
                value = " ".join(value)

            # Check for on* event handlers
            if _ON_ATTR_RE.match(attr):
                violations.append(
                    f"{path.name}: JS event attribute '{attr}' on <{tag.name}>"
                )

            # Check href/src/action for javascript: URIs and .js references
            if attr in ("href", "src", "action") and isinstance(value, str):
                stripped = value.strip().lower()
                if stripped.startswith("javascript:"):
                    violations.append(
                        f"{path.name}: javascript: URI in {attr}='{value[:60]}'"
                    )
                # Check for .js file references (but not style.css etc.)
                base_url = value.split("?")[0]
                if _JS_SRC_RE.search(base_url):
                    violations.append(
                        f"{path.name}: .js file reference in {attr}='{value[:60]}'"
                    )

    return violations


def validate_css_file(path: Path) -> list[str]:
    """
    Check a CSS file for JavaScript-related issues.

    Scans for IE-era CSS expression() calls and attempts a basic parse check
    using tinycss2 if available.

    Args:
        path: Path to the CSS file.

    Returns:
        List of violation strings. Empty = clean.
    """
    violations: list[str] = []

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        violations.append(f"{path.name}: cannot read file — {e}")
        return violations

    # Check for CSS expression() — IE-era JS-in-CSS
    if _CSS_EXPRESSION_RE.search(text):
        violations.append(f"{path.name}: CSS expression() detected (JS in CSS)")

    # Optional: use tinycss2 for parse validation
    try:
        import tinycss2
        rules, _ = tinycss2.parse_stylesheet_bytes(path.read_bytes())
        for rule in rules:
            if rule.type == "error":
                violations.append(f"{path.name}: CSS parse error: {rule.message}")
    except ImportError:
        pass  # tinycss2 is optional

    return violations


def validate(artifact_dir: Path, pages: list[dict]) -> list[str]:
    """
    Run JavaScript validation on all HTML files and style.css.

    Args:
        artifact_dir: Directory containing the generated website files.
        pages:        List of page dicts with 'file' keys.

    Returns:
        List of violation strings. Empty list = all files pass.
    """
    violations: list[str] = []

    # Validate each HTML file
    for page in pages:
        html_path = artifact_dir / page["file"]
        if html_path.exists():
            page_violations = validate_html_file(html_path)
            violations.extend(page_violations)
        # Missing files are handled by structure validator, not here

    # Validate CSS file
    css_path = artifact_dir / "style.css"
    if css_path.exists():
        violations.extend(validate_css_file(css_path))

    if violations:
        logger.warning("JS validation found %d violation(s)", len(violations))
    else:
        logger.info("JS validation passed — no JavaScript detected")

    return violations
