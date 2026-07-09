"""
Harbor task assembler — packages generated websites into complete task directories.

Creates the full Harbor-compatible task directory structure:
  task_dir/
  ├── task.toml          — Task metadata (schema_version 1.1)
  ├── instruction.md     — Agent instructions with screenshot paths and hints
  ├── environment/
  │   ├── Dockerfile     — Container image with Chromium + grading deps
  │   └── assets/        — Reference screenshots
  ├── tests/
  │   ├── test.sh        — Verifier entry point
  │   ├── grade.py       — SSIM/pHash grading script
  │   ├── render.py      — Playwright renderer for agent output
  │   └── pages.json     — Page/viewport configuration
  └── solution/
      ├── style.css      — Ground-truth CSS
      └── *.html         — Ground-truth HTML pages

Output directory naming: v1-<config_slug>-<6-char hash>
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Paths for test scripts
RECIPE_DIR = Path(__file__).parent
PROJECT_ROOT = RECIPE_DIR.parent
GRADER_SRC = PROJECT_ROOT / "grader"


def _seed_hex(seed: int) -> str:
    """Generate a 6-character hex hash from a seed for task ID uniqueness."""
    return hashlib.sha256(str(seed).encode()).hexdigest()[:6]


def task_id(config_name: str, recipe_version: str, seed: int) -> str:
    """
    Generate the task directory name.

    Format: <recipe_version>-<config_slug>-<seed_hash>
    Example: v1-aistartupneonhardconfig-73475c
    """
    slug = config_name.lower().replace("_", "").replace(" ", "")
    return f"{recipe_version}-{slug}-{_seed_hex(seed)}"


def _generate_task_toml(
    tid: str,
    config: Any,
    design_spec: dict,
    seed: int,
) -> str:
    """Render task.toml content from config and spec."""
    archetype = getattr(config, "ARCHETYPE", "generic")
    viewports_json = json.dumps(getattr(config, "VIEWPORTS", ["desktop"]))

    return f"""\
schema_version = "1.1"

[task]
name = "web-design-bench/{tid}"
description = "Replicate a {archetype} website design from screenshots using HTML and CSS only."
authors = [{{ name = "web-design-bench" }}]
keywords = ["web-design", "html", "css", "replication", "visual", "{archetype}"]

[metadata]
recipe_version = "{getattr(config, 'RECIPE_VERSION', 'v1')}"
config_name    = "{config.__class__.__name__}"
seed           = {seed}
difficulty     = "{getattr(config, 'DIFFICULTY', 'medium')}"
archetype      = "{archetype}"
visual_style   = "{getattr(config, 'VISUAL_STYLE', 'clean')}"
viewports      = {viewports_json}
ssim_weight    = {getattr(config, 'SSIM_WEIGHT', 0.6)}
phash_weight   = {getattr(config, 'PHASH_WEIGHT', 0.4)}

[verifier]
timeout_sec = 300.0

[agent]
timeout_sec = 900.0

[environment]
build_timeout_sec = 600.0
os = "linux"
cpus = 2
memory_mb = 3072
storage_mb = 10240
allow_internet = true
"""


def _generate_instruction_md(
    config: Any,
    pages: list[dict],
    scroll_heights: dict[str, int] | None,
    design_spec: dict,
) -> str:
    """Render instruction.md with screenshot paths, design hints, and requirements."""
    viewports = getattr(config, "VIEWPORTS", ["desktop"])
    fmt = getattr(config, "SCREENSHOT_FMT", "png")
    viewport_width = getattr(config, "VIEWPORT_SIZES", {}).get(
        viewports[0] if viewports else "desktop", {}
    ).get("width", 1280)
    animation_frames_ms = getattr(config, "ANIMATION_FRAMES_MS", None)

    fonts = design_spec.get("fonts", [])
    colors = design_spec.get("colors", {})

    lines: list[str] = []
    lines.append("# Website Design Replication Task")
    lines.append("")
    lines.append("You are a Claude Code agent running inside a container. Your goal is to "
                  "**replicate a multi-page website design as faithfully as possible** using "
                  "**HTML and CSS only** — no JavaScript.")
    lines.append("")

    # Step 1: Screenshots and Videos
    lines.append("## Step 1 — View the Reference Assets")
    lines.append("")
    lines.append("Read each of the following files to see the target design. "
                  "Use the `Read` tool on each path:")
    lines.append("")
    for page in pages:
        for vp in viewports:
            lines.append(f"- `/app/assets/{page['name']}_{vp}.{fmt}` — {page['label']} ({vp})")
            if animation_frames_ms:
                lines.append(f"- `/app/assets/{page['name']}_{vp}.webm` — {page['label']} Animation Video ({vp})")
    lines.append("")
    lines.append("Study each asset carefully before writing any code. Note the color "
                  "palette, typography, layout structure, spacing, and UI components on each page.")
    if animation_frames_ms:
        lines.append("Pay special attention to the WebM videos to observe the CSS animations (easing, duration, stagger, and initial hidden states).")
    lines.append("")

    # Step 2: Design info
    lines.append("## Step 2 — Design Information")
    lines.append("")
    lines.append(f"**Viewport width**: {viewport_width}px CSS pixels (set this as your rendering target)")

    if getattr(config, "HINT_SCROLL_HEIGHT", True) and scroll_heights:
        lines.append("")
        lines.append(f"**Reference page heights** (CSS pixels at {viewport_width}px wide):")
        for page in pages:
            for vp in viewports:
                key = f"{page['name']}_{vp}"
                if key in scroll_heights:
                    lines.append(f"- `{page['file']}`: {scroll_heights[key]}px")

    if getattr(config, "HINT_FONTS", True) and fonts:
        lines.append("")
        lines.append("**Fonts used in this design**:")
        for font in fonts:
            lines.append(f"- {font}")
        lines.append("(Embed these as web-safe fallbacks or system fonts — "
                      "no external CDN/Google Fonts links)")

    if getattr(config, "HINT_COLORS", True) and colors:
        lines.append("")
        lines.append("**Color palette**:")
        for name, value in colors.items():
            lines.append(f"- `{name}`: `{value}`")

    lines.append("")

    # Step 3: Plan
    lines.append("## Step 3 — Plan")
    lines.append("")
    lines.append("Before writing code, briefly describe the design system you observe:")
    lines.append("- Layout patterns (grid, flexbox, columns)")
    lines.append("- Shared components (nav, footer, cards)")
    lines.append("- Spacing and typography scale")
    if animation_frames_ms:
        lines.append("- CSS Animations (keyframes, transitions, initial states)")
    lines.append("")

    # Step 4: Code
    lines.append("## Step 4 — Write the Code")
    lines.append("")
    lines.append("Create the following files in `/app/output/`:")
    lines.append("")
    lines.append("```")
    lines.append("/app/output/")
    for page in pages:
        lines.append(f"├── {page['file']}  ({page['label']})")
    lines.append("└── style.css       (Shared stylesheet — all pages link to this)")
    lines.append("```")
    lines.append("")
    lines.append("### Requirements")
    lines.append("")
    lines.append("1. **HTML and CSS only** — no JavaScript (`<script>` tags, `.js` files, "
                  "`onclick` attributes are all forbidden)")
    lines.append(f"2. **Single shared stylesheet** at `/app/output/style.css` — every HTML file "
                  f"must include `<link rel=\"stylesheet\" href=\"style.css\">`")
    lines.append(f"3. **Consistent navigation** on every page with relative links to all "
                  f"{len(pages)} pages")
    lines.append("4. **Match the visual design closely**: colors, fonts, spacing, section "
                  "structure, decorative elements")
    if animation_frames_ms:
        lines.append("5. **Match the CSS animations**: ensure elements animate exactly as seen in the WebM videos (e.g. fade-in, slide-up, stagger). Elements must start in their correct initial state (e.g. opacity 0) before animating.")
    lines.append("6. **Self-contained**: no external CDN links — embed all styles in `style.css`")
    lines.append("7. **Do not modify any files in `/tests/`** — they are used to verify your output")
    lines.append("8. Write files using the `Write` tool directly to `/app/output/<filename>`")
    lines.append("")
    lines.append("### Validation")
    lines.append("")
    lines.append("You can validate your output at any time by running:")
    lines.append("```bash")
    lines.append("bash /tests/test.sh")
    lines.append("```")
    lines.append("The verifier will report which files are missing and display a reward score.")
    lines.append("Aim for a score as close to 1.0 as possible.")
    lines.append("")
    lines.append("Start by reading all reference assets, then write `style.css`, "
                  "then each HTML page.")

    return "\n".join(lines)


def _generate_dockerfile() -> str:
    """Generate the Dockerfile for the task environment."""
    return """\
FROM python:3.11-slim

# Install system packages:
#   - fonts-liberation: clean Latin fonts for consistent rendering
#   - libglib2.0-0 etc: Chromium runtime deps needed by Playwright's bundled browser
RUN apt-get update && apt-get install -y --no-install-recommends \\
    fonts-liberation \\
    libglib2.0-0 \\
    libnss3 \\
    libatk1.0-0 \\
    libatk-bridge2.0-0 \\
    libcups2 \\
    libdrm2 \\
    libxkbcommon0 \\
    libxcomposite1 \\
    libxdamage1 \\
    libxfixes3 \\
    libxrandr2 \\
    libgbm1 \\
    libasound2 \\
    libpangocairo-1.0-0 \\
    libpango-1.0-0 \\
    libcairo2 \\
    libdbus-1-3 \\
    libx11-xcb1 \\
    && rm -rf /var/lib/apt/lists/*

# Install uv for Python package management
RUN pip install --no-cache-dir uv

# Install Python grader dependencies via uv into the system Python
RUN uv pip install --system \\
    playwright==1.44.0 \\
    scikit-image==0.23.2 \\
    Pillow==10.3.0 \\
    numpy==1.26.4 \\
    imagehash==4.3.1 \\
    opencv-python-headless==4.9.0.80

# Install Playwright's bundled Chromium (version-matched to playwright==1.44.0)
RUN playwright install chromium

# Create required directories
RUN mkdir -p /app/assets /app/output /logs/verifier /logs/agent /tests

# Copy reference screenshots into the image.
# NOTE: Harbor uses environment/ as the Docker build context,
# so assets must be placed at environment/assets/ (not task root assets/).
# The pipeline will populate this directory per task before building.
COPY assets/ /app/assets/

WORKDIR /app
"""


def assemble(
    config: Any,
    design_spec: dict,
    solution_dir: Path,
    screenshots_dir: Path,
    pages: list[dict],
    output_root: Path,
    scroll_heights: dict[str, int] | None = None,
    seed: int | None = None,
) -> Path:
    """
    Assemble a complete Harbor-compatible task directory.

    Args:
        config:          A GenerationConfig instance.
        design_spec:     DesignSpec dict (embedded in task.toml metadata).
        solution_dir:    Directory containing ground-truth HTML/CSS.
        screenshots_dir: Directory containing reference screenshots.
        pages:           List of page dicts.
        output_root:     Parent directory for all tasks (typically project_root/tasks/).
        scroll_heights:  Optional dict of page scroll heights from screenshotter.
        seed:            Seed value (falls back to config.SEED).

    Returns:
        Path to the assembled task directory.
    """
    effective_seed = seed if seed is not None else getattr(config, "SEED", 42)
    tid = task_id(
        config.__class__.__name__,
        getattr(config, "RECIPE_VERSION", "v1"),
        effective_seed,
    )
    task_dir = output_root / tid
    task_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Assembling task: %s", tid)

    # ── task.toml ────────────────────────────────────────────────────────────
    task_toml = _generate_task_toml(tid, config, design_spec, effective_seed)
    (task_dir / "task.toml").write_text(task_toml)
    logger.info("  Wrote task.toml")

    # ── instruction.md ───────────────────────────────────────────────────────
    instruction_md = _generate_instruction_md(
        config, pages, scroll_heights, design_spec
    )
    (task_dir / "instruction.md").write_text(instruction_md)
    logger.info("  Wrote instruction.md")

    # ── solution/ ────────────────────────────────────────────────────────────
    sol_dst = task_dir / "solution"
    if sol_dst.resolve() == solution_dir.resolve():
        logger.info("  Solution dir is already in place — skipping copy")
    else:
        if sol_dst.exists():
            shutil.rmtree(sol_dst)
        shutil.copytree(solution_dir, sol_dst)
        logger.info("  Copied solution/ (%d files)", len(list(sol_dst.iterdir())))

    # ── environment/assets/ ──────────────────────────────────────────────────
    env_dir = task_dir / "environment"
    env_dir.mkdir(exist_ok=True)

    assets_dst = env_dir / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(screenshots_dir, assets_dst)
    logger.info("  Copied environment/assets/")

    # ── environment/Dockerfile ───────────────────────────────────────────────
    dockerfile_content = _generate_dockerfile()
    (env_dir / "Dockerfile").write_text(dockerfile_content)
    logger.info("  Wrote Dockerfile")

    # ── tests/ ───────────────────────────────────────────────────────────────
    tests_dir = task_dir / "tests"
    tests_dir.mkdir(exist_ok=True)

    # Write pages.json
    pages_cfg = {
        "pages":            pages,
        "viewports":        getattr(config, "VIEWPORT_SIZES", {}),
        "active_viewports": getattr(config, "VIEWPORTS", ["desktop"]),
        "screenshot_fmt":   getattr(config, "SCREENSHOT_FMT", "png"),
        "ssim_weight":      getattr(config, "SSIM_WEIGHT", 0.6),
        "phash_weight":     getattr(config, "PHASH_WEIGHT", 0.4),
        "dom_iou_weight":   getattr(config, "DOM_IOU_WEIGHT", 0.0),
    }
    if getattr(config, "ANIMATION_FRAMES_MS", None):
        pages_cfg["animation_frames_ms"] = config.ANIMATION_FRAMES_MS
        pages_cfg["static_weight"] = getattr(config, "STATIC_WEIGHT", 0.6)
        pages_cfg["animation_weight"] = getattr(config, "ANIMATION_WEIGHT", 0.4)

    if scroll_heights:
        pages_cfg["scroll_heights"] = scroll_heights

    (tests_dir / "pages.json").write_text(json.dumps(pages_cfg, indent=2))
    logger.info("  Wrote tests/pages.json")

    # Copy test scripts from grader module
    for script in ("grade.py", "render.py", "text_recall.py"):
        src = GRADER_SRC / script
        if src.exists():
            shutil.copy2(src, tests_dir / script)
            logger.info("  Copied tests/%s", script)

    test_sh = GRADER_SRC / "test_template" / "test.sh"
    if test_sh.exists():
        shutil.copy2(test_sh, tests_dir / "test.sh")
        (tests_dir / "test.sh").chmod(0o755)
        logger.info("  Copied tests/test.sh")

    logger.info("Task assembled at: %s", task_dir)
    return task_dir
