"""
Complexity tier checker — DOM and CSS metric validation.

Measures structural complexity of generated HTML/CSS and verifies that it
falls within the expected bounds for the target difficulty tier.

Metrics measured:
  - dom_depth:     Maximum nesting depth across all HTML files
  - unique_tags:   Number of distinct HTML tag names used
  - flexbox_uses:  Count of display: flex / inline-flex in CSS
  - grid_uses:     Count of display: grid / inline-grid in CSS
  - media_queries: Count of @media rules in CSS

Each difficulty tier (easy, medium, hard) has min/max bounds. Values outside
bounds are reported as warnings (not hard rejects) since complexity is
a soft signal of design quality.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ── Tier bounds ──────────────────────────────────────────────────────────────
TIER_BOUNDS: dict[str, dict[str, dict[str, int]]] = {
    "easy": {
        "dom_depth":     {"min": 3,  "max": 7},
        "unique_tags":   {"min": 5,  "max": 12},
        "flexbox_uses":  {"min": 1,  "max": 8},
        "grid_uses":     {"min": 0,  "max": 3},
        "media_queries": {"min": 0,  "max": 2},
    },
    "medium": {
        "dom_depth":     {"min": 5,  "max": 10},
        "unique_tags":   {"min": 8,  "max": 20},
        "flexbox_uses":  {"min": 3,  "max": 18},
        "grid_uses":     {"min": 1,  "max": 8},
        "media_queries": {"min": 1,  "max": 4},
    },
    "hard": {
        "dom_depth":     {"min": 7,  "max": 15},
        "unique_tags":   {"min": 12, "max": 30},
        "flexbox_uses":  {"min": 8,  "max": 45},
        "grid_uses":     {"min": 3,  "max": 18},
        "media_queries": {"min": 2,  "max": 10},
    },
}

# ── CSS metric regexes ──────────────────────────────────────────────────────
_FLEXBOX_RE = re.compile(r"display\s*:\s*(inline-)?flex", re.IGNORECASE)
_GRID_RE    = re.compile(r"display\s*:\s*(inline-)?grid", re.IGNORECASE)
_MEDIA_RE   = re.compile(r"@media\s", re.IGNORECASE)


def _measure_dom_depth(soup: BeautifulSoup) -> int:
    """Calculate maximum nesting depth of the DOM tree."""
    def _depth(element, current: int = 0) -> int:
        max_d = current
        for child in element.children:
            if hasattr(child, 'children'):
                max_d = max(max_d, _depth(child, current + 1))
        return max_d
    return _depth(soup)


def _measure_unique_tags(soup: BeautifulSoup) -> set[str]:
    """Collect all unique HTML tag names in the document."""
    return {tag.name for tag in soup.find_all(True)}


def _measure_css_metrics(css_text: str) -> dict[str, int]:
    """Count CSS layout feature usage."""
    return {
        "flexbox_uses":  len(_FLEXBOX_RE.findall(css_text)),
        "grid_uses":     len(_GRID_RE.findall(css_text)),
        "media_queries": len(_MEDIA_RE.findall(css_text)),
    }


def measure(artifact_dir: Path, pages: list[dict]) -> dict[str, int]:
    """
    Measure complexity metrics for the generated website.

    Args:
        artifact_dir: Directory containing generated HTML/CSS files.
        pages:        List of page dicts with 'file' keys.

    Returns:
        Dict of metric_name -> measured_value.
    """
    max_depth = 0
    all_tags: set[str] = set()

    for page in pages:
        html_path = artifact_dir / page["file"]
        if not html_path.exists():
            continue

        try:
            text = html_path.read_text(encoding="utf-8", errors="replace")
            soup = BeautifulSoup(text, "html.parser")
            depth = _measure_dom_depth(soup)
            max_depth = max(max_depth, depth)
            all_tags.update(_measure_unique_tags(soup))
        except Exception as e:
            logger.warning("Error measuring %s: %s", page["file"], e)

    css_metrics = {"flexbox_uses": 0, "grid_uses": 0, "media_queries": 0}
    css_path = artifact_dir / "style.css"
    if css_path.exists():
        try:
            css_text = css_path.read_text(encoding="utf-8", errors="replace")
            css_metrics = _measure_css_metrics(css_text)
        except Exception as e:
            logger.warning("Error measuring style.css: %s", e)

    metrics = {
        "dom_depth":     max_depth,
        "unique_tags":   len(all_tags),
        **css_metrics,
    }

    logger.info("Complexity metrics: %s", metrics)
    return metrics


def validate(
    artifact_dir: Path,
    pages: list[dict],
    difficulty: str = "medium",
) -> dict[str, dict[str, int]]:
    """
    Check DOM/CSS complexity against tier bounds.

    Args:
        artifact_dir: Directory containing generated HTML/CSS files.
        pages:        List of page dicts with 'file' keys.
        difficulty:   Target difficulty tier ('easy', 'medium', 'hard').

    Returns:
        Empty dict on pass.
        On failure: {metric: {"actual": v, "min": lo, "max": hi}, ...}
        for each metric that falls outside tier bounds.
    """
    bounds = TIER_BOUNDS.get(difficulty, TIER_BOUNDS["medium"])
    metrics = measure(artifact_dir, pages)
    diff: dict[str, dict[str, int]] = {}

    for metric_name, value in metrics.items():
        if metric_name not in bounds:
            continue
        lo = bounds[metric_name]["min"]
        hi = bounds[metric_name]["max"]
        if value < lo or value > hi:
            diff[metric_name] = {"actual": value, "min": lo, "max": hi}
            logger.warning(
                "Complexity %s=%d outside [%d, %d] for %s tier",
                metric_name, value, lo, hi, difficulty,
            )

    if not diff:
        logger.info("Complexity check passed for %s tier", difficulty)

    return diff
