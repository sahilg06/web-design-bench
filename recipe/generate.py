"""
CLI entry point — generate new Harbor tasks from a GenerationConfig + seed.

Usage:
    python -m recipe.generate --config ai_startup_neon_hard [--seed 42] [--count 1]
    python -m recipe.generate --config luxury_fashion_serif_medium --solution-dir /path/to/solution
    python -m recipe.generate --list  # Show all available configs

For each seed:
  1. Build DesignSpec from config (deterministic)
  2. Call generation agent (Claude API) -> HTML/CSS files, OR use --solution-dir
  3. Validate artifacts (JS hard-reject, structural, complexity)
  4. Capture full-page reference screenshots via Playwright
  5. Assemble task directory under tasks/

Human reviews and registers in eval/configs/ after generation.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("recipe.generate")


def _resolve_api_key() -> str:
    """
    Resolve the Anthropic API key from environment or macOS Keychain.

    Returns:
        The API key string.

    Exits:
        With error message if no key can be found.
    """
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

    if not key:
        # Try macOS Keychain
        try:
            result = subprocess.run(
                ["security", "find-generic-password",
                 "-s", "anthropic-api-key",
                 "-a", os.environ.get("USER", ""),
                 "-w"],
                capture_output=True, text=True,
            )
            key = result.stdout.strip()
        except Exception:
            pass

    if not key:
        sys.exit(
            "ERROR: ANTHROPIC_API_KEY not set and not found in macOS Keychain.\n"
            "  Set it: export ANTHROPIC_API_KEY='your-key'\n"
            "  Or store in Keychain: security add-generic-password "
            "-s 'anthropic-api-key' -a \"$USER\" -w '<key>'"
        )

    os.environ["ANTHROPIC_API_KEY"] = key
    return key


def main(argv: list[str] | None = None) -> int:
    """
    Main CLI entry point for task generation.

    Args:
        argv: Command-line arguments (defaults to sys.argv).

    Returns:
        Exit code (0 = success, 1 = failure).
    """
    parser = argparse.ArgumentParser(
        prog="python -m recipe.generate",
        description="Generate Harbor tasks for web-design-bench.",
    )
    parser.add_argument(
        "--config", required=False,
        help="Registered GenerationConfig name (e.g. ai_startup_neon_hard)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Override the config's SEED value",
    )
    parser.add_argument(
        "--count", type=int, default=1,
        help="Number of tasks to generate (seeds: SEED, SEED+1, ...)",
    )
    parser.add_argument(
        "--tasks-dir", default=str(PROJECT_ROOT / "tasks"),
        help="Root directory where task folders are created",
    )
    parser.add_argument(
        "--solution-dir", default=None,
        help="Skip the generation agent; use a pre-built solution/ directory",
    )
    parser.add_argument(
        "--keep-tmp", action="store_true",
        help="Do not delete temp directories after packaging",
    )
    parser.add_argument(
        "--skip-screenshots", action="store_true",
        help="Skip screenshot capture (useful for CI/testing)",
    )
    parser.add_argument(
        "--list", action="store_true", dest="list_configs",
        help="List all available configs and exit",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # ── Import and register all configs ──────────────────────────────────
    import recipe.configs.library  # noqa: F401 — registers all 10 configs
    from recipe.configs import list_configs, load_config

    if args.list_configs:
        print("Available configs:")
        for name in list_configs():
            cfg = load_config(name)
            print(f"  {name:40s} {cfg.ARCHETYPE:20s} {cfg.DIFFICULTY}")
        return 0

    if not args.config:
        parser.error("--config is required (use --list to see available configs)")

    # ── Resolve API key (only needed if generating) ──────────────────────
    if not args.solution_dir:
        _resolve_api_key()

    from recipe import spec as spec_mod
    from recipe.validators import javascript as js_val
    from recipe.validators import structure as struct_val
    from recipe.validators import complexity as cmp_val
    from recipe.packager import assemble

    config = load_config(args.config)
    base_seed = args.seed if args.seed is not None else getattr(config, "SEED", 42)
    tasks_dir = Path(args.tasks_dir)
    tasks_dir.mkdir(parents=True, exist_ok=True)

    generated: list[Path] = []

    for i in range(args.count):
        seed = base_seed + i
        print(f"\n{'='*62}")
        print(f"  Config : {args.config}  |  Seed : {seed}  ({i+1}/{args.count})")
        print(f"{'='*62}")

        # ── Step 1: Build DesignSpec ─────────────────────────────────────
        design_spec = spec_mod.generate(config, seed=seed)
        pages = design_spec.get("pages", [])
        if not pages:
            print("  ERROR: design_spec has no pages — check config.PAGES")
            continue

        # ── Step 2: Generate or load solution ────────────────────────────
        tmp_solution: Path | None = None

        if args.solution_dir:
            solution_dir = Path(args.solution_dir)
            if not solution_dir.exists():
                print(f"  ERROR: solution directory not found: {solution_dir}")
                continue
        else:
            tmp_solution = Path(tempfile.mkdtemp(
                prefix=f"bench_sol_{args.config}_"
            ))
            try:
                from recipe.agent import generate_website
                logger.info("Generating website via Claude API...")
                generate_website(
                    spec=design_spec,
                    output_dir=tmp_solution,
                )
                solution_dir = tmp_solution
            except Exception as exc:
                print(f"  ERROR: generation agent failed: {exc}")
                if not args.keep_tmp and tmp_solution:
                    shutil.rmtree(tmp_solution, ignore_errors=True)
                continue

        # ── Step 3: Validate ─────────────────────────────────────────────
        print("\n[1/3] Validating artifacts ...")

        js_violations = js_val.validate(solution_dir, pages)
        struct_violations = struct_val.validate(solution_dir, pages)

        all_violations = js_violations + struct_violations
        if all_violations:
            print(f"  FAIL: {len(all_violations)} violation(s):")
            for v in all_violations:
                print(f"    • {v}")
            if not args.keep_tmp and tmp_solution:
                shutil.rmtree(tmp_solution, ignore_errors=True)
            continue
        print("  OK: JS + structure validation passed")

        cmp_diff = cmp_val.validate(
            solution_dir, pages,
            getattr(config, "DIFFICULTY", "medium"),
        )
        if cmp_diff:
            print(f"  WARN: complexity check flagged metrics: {list(cmp_diff.keys())}")
            for metric, info in cmp_diff.items():
                print(f"    {metric}: actual={info['actual']} "
                      f"(expected [{info['min']}, {info['max']}])")

        # ── Step 4: Screenshots ──────────────────────────────────────────
        scroll_heights: dict[str, int] = {}
        tmp_screens = Path(tempfile.mkdtemp(prefix=f"bench_shots_{args.config}_"))

        if not args.skip_screenshots:
            print("\n[2/3] Capturing reference screenshots ...")
            try:
                from recipe.capture import capture
                scroll_heights = capture(
                    html_dir=solution_dir,
                    output_dir=tmp_screens / "assets",
                    pages=pages,
                    viewport_width=getattr(config, "VIEWPORT_SIZES", {}).get(
                        "desktop", {}
                    ).get("width", 1280),
                    viewport_height=getattr(config, "VIEWPORT_SIZES", {}).get(
                        "desktop", {}
                    ).get("height", 800),
                    screenshot_fmt=getattr(config, "SCREENSHOT_FMT", "png"),
                    animation_frames_ms=getattr(config, "ANIMATION_FRAMES_MS", None),
                )
                print(f"  OK: {len(scroll_heights)} screenshots captured")
            except ImportError as e:
                print(f"  WARN: Screenshot capture skipped ({e})")
                print("  Creating empty assets directory...")
                (tmp_screens / "assets").mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                print(f"  ERROR: screenshot capture failed: {exc}")
                if not args.keep_tmp:
                    shutil.rmtree(tmp_screens, ignore_errors=True)
                    if tmp_solution:
                        shutil.rmtree(tmp_solution, ignore_errors=True)
                continue
        else:
            print("\n[2/3] Skipping screenshots (--skip-screenshots)")
            (tmp_screens / "assets").mkdir(parents=True, exist_ok=True)

        # ── Step 5: Assemble task ────────────────────────────────────────
        print("\n[3/3] Assembling task directory ...")
        task_dir = assemble(
            config=config,
            design_spec=design_spec,
            solution_dir=solution_dir,
            screenshots_dir=tmp_screens / "assets",
            pages=pages,
            output_root=tasks_dir,
            scroll_heights=scroll_heights,
            seed=seed,
        )
        generated.append(task_dir)
        print(f"\n  ✓ Task ready: {task_dir.name}")
        print("    Review screenshots + solution, then add to eval/configs/ if satisfied.")

        # ── Cleanup ──────────────────────────────────────────────────────
        if not args.keep_tmp:
            shutil.rmtree(tmp_screens, ignore_errors=True)
            if tmp_solution:
                shutil.rmtree(tmp_solution, ignore_errors=True)

    # ── Summary ──────────────────────────────────────────────────────────
    print(f"\n{'='*62}")
    print(f"  Generated {len(generated)}/{args.count} tasks:")
    for p in generated:
        print(f"    {p}")
    print(f"{'='*62}")
    return 0 if generated else 1


if __name__ == "__main__":
    sys.exit(main())
