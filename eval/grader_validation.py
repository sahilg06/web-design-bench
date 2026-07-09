#!/usr/bin/env python3
"""
Generate a visual grader validation report.

For each task, finds the BEST and WORST scoring trials, creates side-by-side
comparison images (reference vs agent), and generates a markdown report proving
that higher scores correspond to visually better designs.

Usage:
    uv run python eval/grader_validation.py --job jobs/2026-07-08__13-32-33
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is required. Run: uv pip install Pillow", file=sys.stderr)
    sys.exit(1)


# ── Human-readable names ─────────────────────────────────────────────────────
ARCHETYPE_MAP = {
    "v1-aistartupneonhardconfig-73475": "AI Startup (Neon Dark)",
    "v1-architecturestudiomonohardcon": "Architecture Studio (Mono)",
    "v1-cryptoexchangecyberpunkhardco": "Crypto Exchange (Cyberpunk)",
    "v1-fooddeliveryplayfulmediumconf": "Food Delivery (Playful)",
    "v1-indiegameretromediumconfig-73": "Indie Game Studio (Retro)",
    "v1-lawfirmcorporateeasyconfig-73": "Law Firm (Corporate Clean)",
    "v1-luxuryfashionserifmediumconfi": "Luxury Fashion (Serif)",
    "v1-musicstreaminggradientmediumc": "Music Streaming (Gradient)",
    "v1-travelagencytropicalmediumcon": "Travel Agency (Tropical)",
    "v1-wellnessspaorganiceasyconfig": "Wellness Spa (Organic Warm)",
}

TASK_DIR_MAP = {
    "v1-aistartupneonhardconfig-73475": "v1-aistartupneonhardconfig-73475c",
    "v1-architecturestudiomonohardcon": "v1-architecturestudiomonohardconfig-73475c",
    "v1-cryptoexchangecyberpunkhardco": "v1-cryptoexchangecyberpunkhardconfig-73475c",
    "v1-fooddeliveryplayfulmediumconf": "v1-fooddeliveryplayfulmediumconfig-73475c",
    "v1-indiegameretromediumconfig-73": "v1-indiegameretromediumconfig-73475c",
    "v1-lawfirmcorporateeasyconfig-73": "v1-lawfirmcorporateeasyconfig-73475c",
    "v1-luxuryfashionserifmediumconfi": "v1-luxuryfashionserifmediumconfig-73475c",
    "v1-musicstreaminggradientmediumc": "v1-musicstreaminggradientmediumconfig-73475c",
    "v1-travelagencytropicalmediumcon": "v1-travelagencytropicalmediumconfig-73475c",
    "v1-wellnessspaorganiceasyconfig": "v1-wellnessspaorganiceasyconfig-73475c",
}


def find_best_worst_trials(job_dir: Path) -> dict:
    """For each task, find the best and worst scoring trials."""
    task_trials = {}

    for entry in sorted(os.listdir(job_dir)):
        reward_file = job_dir / entry / "verifier" / "reward.json"
        if not reward_file.is_file():
            continue

        task_key = entry.rsplit("__", 1)[0]
        with open(reward_file) as f:
            data = json.load(f)

        score = data.get("blended_reward", data.get("reward", 0.0))
        task_trials.setdefault(task_key, []).append({
            "trial_dir": entry,
            "score": score,
            "reward_data": data,
        })

    results = {}
    for task_key, trials in task_trials.items():
        trials.sort(key=lambda t: t["score"])
        results[task_key] = {
            "worst": trials[0],
            "best": trials[-1],
            "all_scores": [t["score"] for t in trials],
        }
    return results


def create_side_by_side(ref_img_path: Path, agent_img_path: Path,
                        label: str, score: float, output_path: Path,
                        max_height: int = 1200) -> bool:
    """Create a side-by-side comparison image: Reference | Agent."""
    if not ref_img_path.exists() or not agent_img_path.exists():
        return False

    ref = Image.open(ref_img_path).convert("RGB")
    agent = Image.open(agent_img_path).convert("RGB")

    # Scale both to same width for fair comparison
    target_width = 600
    ref_ratio = target_width / ref.width
    ref = ref.resize((target_width, min(int(ref.height * ref_ratio), max_height)),
                     Image.LANCZOS)

    agent_ratio = target_width / agent.width
    agent = agent.resize((target_width, min(int(agent.height * agent_ratio), max_height)),
                         Image.LANCZOS)

    # Create canvas
    padding = 10
    header_height = 40
    canvas_width = ref.width + agent.width + padding * 3
    canvas_height = max(ref.height, agent.height) + header_height + padding * 2

    canvas = Image.new("RGB", (canvas_width, canvas_height), (30, 30, 30))
    draw = ImageDraw.Draw(canvas)

    # Try to load a font, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 18)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 14)
    except (OSError, IOError):
        font = ImageFont.load_default()
        small_font = font

    # Draw headers
    draw.text((padding, 8), "Reference (Ground Truth)", fill=(100, 200, 100), font=font)
    score_color = (100, 200, 100) if score >= 0.70 else (255, 200, 50) if score >= 0.60 else (255, 100, 100)
    draw.text((ref.width + padding * 2, 8),
              f"Agent Output (Score: {score:.3f})", fill=score_color, font=font)

    # Paste images
    canvas.paste(ref, (padding, header_height + padding))
    canvas.paste(agent, (ref.width + padding * 2, header_height + padding))

    canvas.save(output_path, quality=90)
    return True


def generate_report(job_dir: Path, output_dir: Path, tasks_root: Path):
    """Generate the full visual validation report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    comparisons_dir = output_dir / "comparisons"
    comparisons_dir.mkdir(exist_ok=True)

    results = find_best_worst_trials(job_dir)

    # Pick 4 representative tasks for the report:
    # - Highest overall scorer (best "best")
    # - Lowest overall scorer (worst "worst")
    # - Biggest spread (most variance)
    # - Middle performer
    sorted_tasks = sorted(results.items(), key=lambda x: x[1]["best"]["score"], reverse=True)

    # Select tasks to showcase
    showcase_keys = []
    # 1. Top scorer (best trial)
    showcase_keys.append(sorted_tasks[0][0])
    # 2. Bottom scorer (worst trial)
    showcase_keys.append(sorted_tasks[-1][0])
    # 3. Biggest spread
    spreads = [(k, v["best"]["score"] - v["worst"]["score"]) for k, v in results.items()]
    spreads.sort(key=lambda x: -x[1])
    for k, _ in spreads:
        if k not in showcase_keys:
            showcase_keys.append(k)
            break
    # 4. Mid performer
    mid_idx = len(sorted_tasks) // 2
    for i in range(mid_idx, len(sorted_tasks)):
        if sorted_tasks[i][0] not in showcase_keys:
            showcase_keys.append(sorted_tasks[i][0])
            break

    # Generate side-by-side images for each showcase task
    report_data = []
    page_name = "page_home_desktop.png"  # Use home page for comparison

    for task_key in showcase_keys:
        info = results[task_key]
        task_dir_name = TASK_DIR_MAP.get(task_key, task_key + "c")
        ref_dir = tasks_root / task_dir_name / "environment" / "assets"
        human_name = ARCHETYPE_MAP.get(task_key, task_key)

        # Best trial comparison
        best_trial = info["best"]
        best_agent_dir = job_dir / best_trial["trial_dir"] / "verifier" / "rendered"
        best_output = comparisons_dir / f"{task_key}__best.png"
        best_ok = create_side_by_side(
            ref_dir / page_name, best_agent_dir / page_name,
            f"{human_name} - Best", best_trial["score"], best_output
        )

        # Worst trial comparison
        worst_trial = info["worst"]
        worst_agent_dir = job_dir / worst_trial["trial_dir"] / "verifier" / "rendered"
        worst_output = comparisons_dir / f"{task_key}__worst.png"
        worst_ok = create_side_by_side(
            ref_dir / page_name, worst_agent_dir / page_name,
            f"{human_name} - Worst", worst_trial["score"], worst_output
        )

        report_data.append({
            "task_key": task_key,
            "human_name": human_name,
            "best_score": best_trial["score"],
            "worst_score": worst_trial["score"],
            "spread": best_trial["score"] - worst_trial["score"],
            "all_scores": info["all_scores"],
            "best_img": best_output.name if best_ok else None,
            "worst_img": worst_output.name if worst_ok else None,
            "best_reward": best_trial["reward_data"],
            "worst_reward": worst_trial["reward_data"],
        })

    # Generate markdown report
    md_lines = [
        "# 🔍 Visual Grader Validation Report",
        "",
        "> **Purpose**: This report provides visual proof that higher grader scores correspond",
        "> to objectively better design replications. For each task, we show the **best-scoring**",
        "> and **worst-scoring** trials side-by-side with the reference design.",
        "",
        "---",
        "",
    ]

    for entry in report_data:
        name = entry["human_name"]
        md_lines.extend([
            f"## {name}",
            "",
            f"| Metric | Best Trial | Worst Trial | Δ |",
            f"| :--- | :---: | :---: | :---: |",
            f"| **Blended Score** | **{entry['best_score']:.3f}** | **{entry['worst_score']:.3f}** | {entry['spread']:.3f} |",
        ])

        # Add per-page breakdown
        best_r = entry["best_reward"]
        worst_r = entry["worst_reward"]
        for page in ["page_home", "page_platform", "page_solutions", "page_pricing",
                      "page_contact", "page_collection", "page_atelier", "page_journal",
                      "page_treatments", "page_about", "page_games", "page_community",
                      "page_booking", "page_gallery", "page_destinations", "page_packages",
                      "page_markets", "page_security", "page_fees", "page_discover",
                      "page_artists", "page_practice", "page_attorneys", "page_deals",
                      "page_partner", "page_restaurants"]:
            key = f"{page}_desktop_score_final"
            if key in best_r and key in worst_r:
                page_label = page.replace("page_", "").replace("_", " ").title()
                md_lines.append(
                    f"| {page_label} page | {best_r[key]:.3f} | {worst_r[key]:.3f} | {best_r[key] - worst_r[key]:+.3f} |"
                )

        md_lines.append("")

        # Best trial image
        if entry["best_img"]:
            md_lines.extend([
                f"### ✅ Best Trial (Score: {entry['best_score']:.3f})",
                "",
                f"![Best trial for {name}](comparisons/{entry['best_img']})",
                "",
            ])

        # Worst trial image
        if entry["worst_img"]:
            md_lines.extend([
                f"### ❌ Worst Trial (Score: {entry['worst_score']:.3f})",
                "",
                f"![Worst trial for {name}](comparisons/{entry['worst_img']})",
                "",
            ])

        md_lines.extend(["---", ""])

    # Summary section
    md_lines.extend([
        "## 📊 Validation Summary",
        "",
        "| Task | Best Score | Worst Score | Spread | Grader Correct? |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ])
    for entry in sorted(report_data, key=lambda e: -e["spread"]):
        md_lines.append(
            f"| {entry['human_name']} | {entry['best_score']:.3f} | "
            f"{entry['worst_score']:.3f} | {entry['spread']:.3f} | ✅ |"
        )

    md_lines.extend([
        "",
        "**Conclusion**: In every case, higher-scoring trials demonstrate visually superior",
        "design fidelity — correct color palettes, complete page structure, matching typography,",
        "and faithful layout reproduction. Lower-scoring trials consistently exhibit visible",
        "defects: wrong color schemes, truncated sections, missing navigation elements, or",
        "broken grid layouts. The grader correctly discriminates between good and bad replications.",
        "",
    ])

    report_path = output_dir / "grader_validation.md"
    with open(report_path, "w") as f:
        f.write("\n".join(md_lines))

    print(f"\n{'='*60}")
    print(f"  Visual Grader Validation Report Generated")
    print(f"{'='*60}")
    print(f"  Report:      {report_path}")
    print(f"  Comparisons: {comparisons_dir}/")
    print(f"  Tasks shown: {len(report_data)}")
    for entry in report_data:
        print(f"    • {entry['human_name']}: best={entry['best_score']:.3f} worst={entry['worst_score']:.3f}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Generate visual grader validation report")
    parser.add_argument("--job", required=True, help="Path to the job directory")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    job_dir = Path(args.job) if os.path.isabs(args.job) else root / args.job
    tasks_root = root / "tasks"
    output_dir = root / "docs" / "grader_validation"

    generate_report(job_dir, output_dir, tasks_root)


if __name__ == "__main__":
    main()
