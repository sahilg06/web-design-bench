#!/usr/bin/env python3
"""
Playwright-based HTML screenshot renderer for web-design-bench.

Takes HTML files produced by an AI coding agent and renders them to full-page
PNG screenshots using a headless Chromium browser. These screenshots are later
compared against reference screenshots by the visual grader.

Design decisions:
    - Uses async Playwright for efficiency when rendering multiple pages, since
      each page render involves network-idle waits that benefit from concurrency.
    - Reads viewport configuration from pages.json so the same renderer works
      across tasks with different viewport requirements (desktop, tablet, mobile).
    - Renders at device_scale_factor=1 to match reference screenshots pixel-for-pixel.
    - Uses full_page=True to capture below-the-fold content, which is critical for
      evaluating whether the agent reproduced the complete page layout.
    - Falls back to sensible defaults (1280×800) if viewport config is missing.

Container paths (Harbor convention):
    - Agent HTML output:    /app/output/
    - Reference screenshots: /app/assets/
    - Rendered output:       /logs/verifier/rendered/
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


async def render_pages(
    pages_json: Path,
    html_dir: Path,
    output_dir: Path,
) -> int:
    """
    Render all pages defined in pages.json to full-page screenshots.

    Args:
        pages_json: Path to the pages.json configuration file.
        html_dir:   Directory containing the HTML files to render.
        output_dir: Directory where screenshot PNGs will be written.

    Returns:
        Number of rendering errors encountered (0 = success).

    The function iterates over each (page, viewport) combination defined in
    pages.json and produces one screenshot per combination, named as:
        {page_name}_{viewport_name}.{fmt}
    e.g., page_home_desktop.png
    """
    with open(pages_json) as f:
        cfg: dict[str, Any] = json.load(f)

    output_dir.mkdir(parents=True, exist_ok=True)

    screenshot_fmt = cfg.get("screenshot_fmt", "png")
    viewports_def = cfg.get("viewports", {})
    active_viewports = cfg.get(
        "active_viewports", list(viewports_def.keys())
    )
    animation_frames_ms = cfg.get("animation_frames_ms", None)

    # Allow overriding the Chromium binary path via environment variable,
    # which is useful in Docker containers with pre-installed Chromium.
    chromium_path = os.environ.get("CHROMIUM_PATH", None)

    from playwright.async_api import async_playwright

    errors = 0

    async with async_playwright() as pw:
        launch_kwargs: dict[str, Any] = {
            "args": [
                "--no-sandbox",
                "--allow-file-access-from-files",
                "--disable-web-security",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-setuid-sandbox",
            ],
        }
        if chromium_path:
            launch_kwargs["executable_path"] = chromium_path

        browser = await pw.chromium.launch(**launch_kwargs)

        for vp_name in active_viewports:
            vp_cfg = viewports_def.get(vp_name, {"width": 1280, "height": 800})
            vp_width = vp_cfg["width"]
            vp_height = vp_cfg["height"]

            context = await browser.new_context(
                viewport={"width": vp_width, "height": vp_height},
                device_scale_factor=1,
            )

            for idx, page_cfg in enumerate(cfg["pages"]):
                page_name = page_cfg["name"]
                html_file = page_cfg["file"]
                html_path = html_dir / html_file
                out_path = output_dir / f"{page_name}_{vp_name}.{screenshot_fmt}"

                if not html_path.exists():
                    logger.warning("HTML file not found: %s", html_path)
                    errors += 1
                    continue

                url = f"file://{html_path.resolve()}"
                logger.info(
                    "Rendering %s @ %dx%d -> %s (animations: %s)",
                    html_file, vp_width, vp_height, out_path.name, animation_frames_ms is not None,
                )

                try:
                    if animation_frames_ms:
                        # 1. Capture frozen animation frames for grading.
                        for t_ms in animation_frames_ms:
                            frame_page = await context.new_page()
                            await frame_page.goto(url, wait_until="networkidle", timeout=30_000)
                            await frame_page.evaluate(f"""
                                document.getAnimations().forEach(a => {{
                                    a.currentTime = {t_ms};
                                    a.pause();
                                }});
                            """)
                            frame_path = output_dir / f"{page_name}_{vp_name}_t{t_ms}.{screenshot_fmt}"
                            await frame_page.screenshot(path=str(frame_path), full_page=True)
                            await frame_page.close()
                            logger.info("  Captured frozen frame T=%dms -> %s", t_ms, frame_path.name)

                        # 2. Capture settled state (t=2000ms) as main screenshot.
                        settled_page = await context.new_page()
                        await settled_page.goto(url, wait_until="networkidle", timeout=30_000)
                        await settled_page.evaluate("""
                            document.getAnimations().forEach(a => {
                                a.currentTime = 2000;
                                a.pause();
                            });
                        """)
                        await settled_page.screenshot(path=str(out_path), full_page=True)
                        await settled_page.close()

                    else:
                        page = await context.new_page()
                        await page.goto(url, wait_until="networkidle", timeout=30_000)
                        
                        # For SPA pages (all sharing index.html), click the nav tab
                        # to switch to the correct page view.
                        is_spa = all(p["file"] == cfg["pages"][0]["file"] for p in cfg["pages"])
                        if is_spa and idx > 0:
                            label = page_cfg["label"]
                            try:
                                nav_btn = page.get_by_role("button", name=label).or_(
                                    page.get_by_role("link", name=label)
                                ).or_(
                                    page.locator(f"nav >> text='{label}'")
                                )
                                await nav_btn.first.click(timeout=5000)
                                await page.wait_for_timeout(500)
                            except Exception as e:
                                logger.warning("    Could not click nav tab '%s': %s", label, e)

                        await page.wait_for_timeout(500)
                        await page.screenshot(path=str(out_path), full_page=True)
                        await page.close()
                except Exception as exc:
                    logger.error("Failed to render %s: %s", html_file, exc)
                    errors += 1

            await context.close()

        await browser.close()

    return errors


def main() -> int:
    """CLI entry point for the renderer."""
    parser = argparse.ArgumentParser(
        description="Render agent HTML to full-page screenshots via Playwright."
    )
    parser.add_argument(
        "--pages-json", required=True,
        help="Path to pages.json configuration file",
    )
    parser.add_argument(
        "--html-dir", required=True,
        help="Directory containing the agent's HTML output files",
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Directory to write rendered PNG screenshots",
    )
    args = parser.parse_args()

    errors = asyncio.run(
        render_pages(
            pages_json=Path(args.pages_json),
            html_dir=Path(args.html_dir),
            output_dir=Path(args.output_dir),
        )
    )

    if errors:
        logger.warning("%d render error(s) encountered.", errors)
    else:
        logger.info("All pages rendered successfully.")

    # Always return 0 so the pipeline continues to grading even if some
    # pages failed to render (they'll just score 0.0).
    return 0


if __name__ == "__main__":
    sys.exit(main())
