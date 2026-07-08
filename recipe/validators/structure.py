"""
Structural validator — file existence and HTML integrity.

Verifies:
  1. All expected HTML files (from the page list) are present
  2. style.css is present
  3. No unexpected files exist (.js files, extra HTML pages)
  4. Every HTML file links to style.css via <link rel="stylesheet">
  5. Every HTML file parses successfully with BeautifulSoup
  6. Every HTML file has required structural elements (<html>, <head>, <body>)
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_STYLE_LINK_RE = re.compile(
    r'<link[^>]+href=["\']style\.css["\']', re.IGNORECASE
)


def _check_file_presence(
    artifact_dir: Path,
    expected_html: set[str],
) -> list[str]:
    """Check that all required files exist and no unexpected files are present."""
    violations: list[str] = []

    # Check required HTML files
    for f in sorted(expected_html):
        if not (artifact_dir / f).exists():
            violations.append(f"Missing required file: {f}")

    # Check style.css
    if not (artifact_dir / "style.css").exists():
        violations.append("Missing required file: style.css")

    # Check for unexpected files (especially .js)
    all_expected = expected_html | {"style.css"}
    present_files = {p.name for p in artifact_dir.iterdir() if p.is_file()}
    unexpected = present_files - all_expected

    for f in sorted(unexpected):
        if f.endswith(".js"):
            violations.append(f"Forbidden file type: {f} (.js files not allowed)")
        else:
            violations.append(f"Unexpected file: {f}")

    return violations


def _check_html_integrity(
    artifact_dir: Path,
    expected_html: set[str],
) -> list[str]:
    """Verify HTML files parse correctly and have required structure."""
    violations: list[str] = []

    for fname in sorted(expected_html):
        fpath = artifact_dir / fname
        if not fpath.exists():
            continue  # Already reported by _check_file_presence

        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            violations.append(f"{fname}: cannot read — {e}")
            continue

        # Check HTML parses at all
        try:
            soup = BeautifulSoup(text, "html.parser")
        except Exception as e:
            violations.append(f"{fname}: HTML parse error — {e}")
            continue

        # Check for stylesheet link
        links = soup.find_all("link", rel=lambda r: r and "stylesheet" in r)
        linked_css = [link.get("href", "") for link in links]
        if not any("style.css" in href for href in linked_css):
            violations.append(f"{fname}: does not link to style.css")

        # Check for basic HTML structure
        if not soup.find("html"):
            violations.append(f"{fname}: missing <html> element")
        if not soup.find("head"):
            violations.append(f"{fname}: missing <head> element")
        if not soup.find("body"):
            violations.append(f"{fname}: missing <body> element")

        # Check for navigation
        if not soup.find("nav"):
            violations.append(f"{fname}: missing <nav> element")

        # Check for <title> tag
        title = soup.find("title")
        if not title or not title.string or not title.string.strip():
            violations.append(f"{fname}: missing or empty <title> tag")

    return violations


def validate(artifact_dir: Path, pages: list[dict]) -> list[str]:
    """
    Run structural validation on the artifact directory.

    Args:
        artifact_dir: Directory containing the generated website files.
        pages:        List of page dicts with 'file' keys.

    Returns:
        List of violation strings. Empty list = all checks pass.
    """
    expected_html = {p["file"] for p in pages}

    violations: list[str] = []
    violations.extend(_check_file_presence(artifact_dir, expected_html))
    violations.extend(_check_html_integrity(artifact_dir, expected_html))

    if violations:
        logger.warning("Structure validation found %d issue(s)", len(violations))
    else:
        logger.info("Structure validation passed — all files OK")

    return violations
