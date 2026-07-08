"""
Playwright screenshot capture for reference website images.

Renders generated HTML files in a headless Chromium browser at the configured
viewport width and captures full-page screenshots at natural scroll height.

Output convention: page_<name>_<viewport>.png
  e.g. page_home_desktop.png

Also records the CSS pixel scroll height of each page — used for:
  - HINT_SCROLL_HEIGHT in instruction.md (helps agents match content density)
  - height_ratio scoring in the grader

Runs on the HOST machine (not inside a container).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def capture(
    html_dir: Path,
    output_dir: Path,
    pages: list[dict],
    viewport_width: int = 1280,
    viewport_height: int = 800,
    screenshot_fmt: str = "png",
    device_scale_factor: int = 1,
) -> dict[str, int]:
    """
    Capture full-page screenshots of all HTML pages using Playwright.

    Args:
        html_dir:            Directory containing HTML files and style.css.
        output_dir:          Directory to save screenshots into.
        pages:               List of page dicts with 'name' and 'file' keys.
        viewport_width:      Browser viewport width in CSS pixels.
        viewport_height:     Browser viewport height in CSS pixels.
        screenshot_fmt:      Screenshot format ('png' or 'jpeg').
        device_scale_factor: Device pixel ratio (1 for standard, 2 for retina).

    Returns:
        Dict mapping "<page_name>_desktop" -> scroll_height_px.

    Raises:
        ImportError: If playwright is not installed.
        FileNotFoundError: If html_dir does not exist.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ImportError(
            "Playwright is required for screenshot capture. Install with: "
            "pip install playwright && python -m playwright install chromium"
        )

    if not html_dir.exists():
        raise FileNotFoundError(f"HTML directory not found: {html_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    scroll_heights: dict[str, int] = {}

    logger.info(
        "Capturing screenshots: %d pages @ %dx%d",
        len(pages), viewport_width, viewport_height,
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])

        context = browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=device_scale_factor,
        )

        for page_cfg in pages:
            page_name = page_cfg["name"]
            html_file = page_cfg["file"]
            html_path = html_dir / html_file
            out_name = f"{page_name}_desktop.{screenshot_fmt}"
            out_path = output_dir / out_name

            if not html_path.exists():
                logger.warning("SKIP (not found): %s", html_path)
                continue

            url = f"file://{html_path.resolve()}"
            logger.info(
                "  %s @ %dx%d -> %s",
                html_file, viewport_width, viewport_height, out_name,
            )

            pw_page = context.new_page()
            pw_page.goto(url, wait_until="networkidle")

            # Record scroll height
            scroll_h = pw_page.evaluate("document.documentElement.scrollHeight")
            key = f"{page_name}_desktop"
            scroll_heights[key] = scroll_h
            logger.info("    scroll_height = %dpx", scroll_h)

            # Full-page screenshot
            pw_page.screenshot(path=str(out_path), full_page=True)
            pw_page.close()

        context.close()
        browser.close()

    logger.info(
        "Screenshots saved to %s (%d files)",
        output_dir, len(scroll_heights),
    )
    return scroll_heights


def capture_from_config(
    html_dir: Path,
    output_dir: Path,
    pages_json: Path,
    update_heights: bool = False,
) -> dict[str, int]:
    """
    Convenience wrapper that reads config from a pages.json file.

    This mirrors the interface used by the reference implementation's
    screenshotter for compatibility with the task packaging pipeline.

    Args:
        html_dir:       Directory containing HTML files.
        output_dir:     Directory to save screenshots.
        pages_json:     Path to pages.json config file.
        update_heights: If True, writes scroll heights back to pages.json.

    Returns:
        Dict of scroll heights.
    """
    with open(pages_json) as f:
        cfg = json.load(f)

    pages = cfg.get("pages", [])
    fmt = cfg.get("screenshot_fmt", "png")

    viewports = cfg.get("viewports", {})
    active = cfg.get("active_viewports", list(viewports.keys()))
    vp_name = active[0] if active else "desktop"
    vp_cfg = viewports.get(vp_name, {"width": 1280, "height": 800})

    scroll_heights = capture(
        html_dir=html_dir,
        output_dir=output_dir,
        pages=pages,
        viewport_width=vp_cfg["width"],
        viewport_height=vp_cfg["height"],
        screenshot_fmt=fmt,
    )

    if update_heights:
        cfg["scroll_heights"] = scroll_heights
        pages_json.write_text(json.dumps(cfg, indent=2))
        logger.info("Updated scroll_heights in %s", pages_json)

    return scroll_heights
