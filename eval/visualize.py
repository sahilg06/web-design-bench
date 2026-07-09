#!/usr/bin/env python3
"""
Generate publication-quality visualizations from Harbor evaluation jobs.

Usage:
    # Run with dynamically installed matplotlib & seaborn via uv
    uv run --with matplotlib --with seaborn python -m eval.visualize --job jobs/2026-07-08__13-32-33
"""

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
JOBS_DIR = Path(__file__).resolve().parent.parent / "jobs"


def find_latest_job() -> Path:
    """Find the most recent job directory."""
    if not JOBS_DIR.exists():
        print("ERROR: jobs/ directory not found", file=sys.stderr)
        sys.exit(1)

    job_dirs = sorted(
        [d for d in JOBS_DIR.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    if not job_dirs:
        print("ERROR: No job directories found in jobs/", file=sys.stderr)
        sys.exit(1)

    return job_dirs[0]


def generate_plots(job_dir: Path) -> None:
    """Generate and save evaluation plots."""
    if not job_dir.exists():
        print(f"ERROR: Job directory {job_dir} not found.", file=sys.stderr)
        sys.exit(1)

    # Collect per-trial rewards grouped by task
    task_scores: dict[str, list[float]] = {}
    
    for entry in sorted(os.listdir(job_dir)):
        reward_file = job_dir / entry / "verifier" / "reward.json"
        if not reward_file.is_file():
            continue
        with open(reward_file) as f:
            r = json.load(f)
        task_name = entry.rsplit("__", 1)[0]
        score = r.get("blended_reward", r.get("reward", 0.0))
        task_scores.setdefault(task_name, []).append(score)

    if not task_scores:
        print(f"ERROR: No valid trial rewards found in {job_dir}", file=sys.stderr)
        sys.exit(1)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Clean up task names for display
    from eval import get_task_display_name
    clean_scores = {}
    for full_name, scores in task_scores.items():
        short = get_task_display_name(full_name)
        clean_scores[short] = scores

    # Sort tasks by mean score descending
    sorted_tasks = sorted(clean_scores.keys(), key=lambda k: sum(clean_scores[k]) / len(clean_scores[k]), reverse=True)

    # Set seaborn styling
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({"font.size": 12, "figure.autolayout": True})

    # ── PLOT 1: Boxplot of Task Rewards (Variance & Distribution) ─────────────
    plt.figure(figsize=(12, 7))
    plot_data = [clean_scores[t] for t in sorted_tasks]
    
    ax = sns.boxplot(
        data=plot_data,
        orient="h",
        palette="viridis",
        width=0.6,
        flierprops={"marker": "o", "markersize": 6, "markerfacecolor": "red"}
    )
    
    # Overlay individual trial points for transparency
    sns.stripplot(data=plot_data, orient="h", color="black", alpha=0.4, jitter=0.2, size=5)

    plt.title(f"Claude Code Benchmark Performance by Task\n(Job: {job_dir.name} | 10 Trials/Task)", fontsize=16, pad=15, fontweight="bold")
    plt.xlabel("Blended Reward (0.0 = Fail, 1.0 = Perfect Visual Match)", fontsize=14, labelpad=10)
    plt.ylabel("Website Archetype & Difficulty", fontsize=14, labelpad=10)
    plt.xlim(0.4, 0.9)
    ax.set_yticklabels(sorted_tasks)

    # Add vertical line for overall mean
    all_scores = [s for scores in clean_scores.values() for s in scores]
    overall_mean = sum(all_scores) / len(all_scores)
    plt.axvline(overall_mean, color="crimson", linestyle="--", linewidth=2, label=f"Overall Mean ({overall_mean:.3f})")
    plt.legend(loc="upper left")

    job_results_dir = RESULTS_DIR / job_dir.name
    job_results_dir.mkdir(parents=True, exist_ok=True)

    boxplot_path = job_results_dir / "task_variance_boxplot.png"
    plt.savefig(boxplot_path, dpi=300, bbox_inches="tight")
    plt.close()

    # ── PLOT 2: Bar Chart of Mean Rewards ─────────────────────────────────────
    plt.figure(figsize=(12, 6))
    means = [sum(clean_scores[t]) / len(clean_scores[t]) for t in sorted_tasks]
    
    barplot = sns.barplot(
        x=means,
        y=sorted_tasks,
        palette="magma",
        orient="h"
    )

    plt.title(f"Mean Blended Reward by Website Archetype\n(Job: {job_dir.name})", fontsize=16, pad=15, fontweight="bold")
    plt.xlabel("Mean Blended Reward", fontsize=14, labelpad=10)
    plt.xlim(0.0, 1.0)

    # Add value labels on bars
    for i, v in enumerate(means):
        barplot.text(v + 0.01, i + 0.1, f"{v:.3f}", color="black", fontweight="bold")

    barchart_path = job_results_dir / "task_means_barchart.png"
    plt.savefig(barchart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nSUCCESS: Visualizations generated in {job_results_dir}:")
    print(f"  - {boxplot_path.name} (Box plot showing variance across 10 trials)")
    print(f"  - {barchart_path.name} (Bar chart of mean scores)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate evaluation plots from Harbor job results.")
    parser.add_argument("--job", type=str, default=None, help="Path to job directory. Defaults to latest job.")
    args = parser.parse_args()

    job_dir = Path(args.job) if args.job else find_latest_job()
    if not job_dir.is_absolute():
        job_dir = Path.cwd() / job_dir

    generate_plots(job_dir)


if __name__ == "__main__":
    main()
