"""
DesignSpec builder.

Reads design spec fields directly from a GenerationConfig class and produces
a deterministic DesignSpec dictionary. The spec is fully deterministic: same
config + seed always produces the same spec.

The seed is recorded in the spec and reserved for future per-seed variation
of color/font/content within an archetype (e.g., randomizing accent colors
or shuffling page content descriptions).

The returned dict is used by:
  - prompt.py — to render the Claude generation prompt
  - packager.py — to embed design metadata in task.toml
  - instruction.md — to provide design hints to the evaluation agent
"""

from __future__ import annotations

import hashlib
import random
from typing import Any


def generate(config: Any, seed: int | None = None) -> dict[str, Any]:
    """
    Build a DesignSpec dict from a GenerationConfig instance.

    Args:
        config: A GenerationConfig instance (from configs/library.py).
        seed:   Optional seed override. Falls back to config.SEED (default 42).

    Returns:
        A dict containing all design parameters needed for generation,
        packaging, and instruction rendering.
    """
    effective_seed = seed if seed is not None else getattr(config, "SEED", 42)

    spec: dict[str, Any] = {
        # ── Identity ─────────────────────────────────────────────────────
        "archetype":         getattr(config, "ARCHETYPE",         "generic"),
        "visual_style":      getattr(config, "VISUAL_STYLE",      "clean"),
        "difficulty":        getattr(config, "DIFFICULTY",         "medium"),
        "seed":              effective_seed,

        # ── Brand ────────────────────────────────────────────────────────
        "brand_name":        getattr(config, "BRAND_NAME",        "Brand"),
        "brand_tagline":     getattr(config, "BRAND_TAGLINE",     ""),

        # ── Visual system ────────────────────────────────────────────────
        "colors":            dict(getattr(config, "COLORS", {})),
        "fonts":             list(getattr(config, "FONTS",  [])),
        "design_directives": getattr(config, "DESIGN_DIRECTIVES", ""),

        # ── Pages ────────────────────────────────────────────────────────
        "pages":             _resolve_pages(config),

        # ── Rendering config ─────────────────────────────────────────────
        "viewports":         getattr(config, "VIEWPORTS",         ["desktop"]),
        "viewport_sizes":    dict(getattr(config, "VIEWPORT_SIZES", {})),
        "screenshot_fmt":    getattr(config, "SCREENSHOT_FMT",    "png"),

        # ── Scoring weights ──────────────────────────────────────────────
        "ssim_weight":       getattr(config, "SSIM_WEIGHT",       0.6),
        "phash_weight":      getattr(config, "PHASH_WEIGHT",      0.4),
        "dom_iou_weight":    getattr(config, "DOM_IOU_WEIGHT",    0.0),
    }
    return spec


def spec_id(config_name: str, seed: int) -> str:
    """
    Generate a short deterministic identifier for a config+seed combination.

    Used for task directory naming: v1-<config_slug>-<6-char hash>.
    """
    raw = f"{config_name}:{seed}"
    return hashlib.sha256(raw.encode()).hexdigest()[:6]


def _resolve_pages(config: Any) -> list[dict[str, str]]:
    """
    Normalize page definitions from the config into a clean list of dicts.

    Each page dict has exactly: name, file, label, description.
    """
    raw = getattr(config, "PAGES", [])
    pages: list[dict[str, str]] = []
    for p in raw:
        page = {
            "name":        p.get("name",        ""),
            "file":        p.get("file",        ""),
            "label":       p.get("label",       p.get("name", "")),
            "description": p.get("description", ""),
        }
        pages.append(page)
    return pages
