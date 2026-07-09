#!/usr/bin/env python3
"""
Summarize a Harbor evaluation job into a structured results history.

After each `./run_eval.sh` completes, run this script to extract key metrics
and append them to `results/history.csv`. This builds a systematic record
across all evaluation runs for comparison and regression testing.

Usage:
    # Summarize the latest job automatically
    uv run python -m eval.summarize

    # Summarize a specific job
    uv run python -m eval.summarize --job jobs/2026-07-08__13-32-33
"""

import argparse
import csv
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path


RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
HISTORY_CSV = RESULTS_DIR / "history.csv"
JOBS_DIR = Path(__file__).resolve().parent.parent / "jobs"

CSV_COLUMNS = [
    "run_id",
    "timestamp",
    "model",
    "agent",
    "env",
    "n_tasks",
    "n_trials",
    "n_errors",
    "mean_reward",
    "min_reward",
    "max_reward",
    "std_reward",
    "pass_at_1_070",
    "pass_at_5_070",
    "pass_at_10_070",
    "per_task_json",
    "job_path",
]


def _compute_pass_at_k(
    task_scores: dict[str, list[float]], threshold: float, k: int
) -> float:
    """Compute unbiased pass@k across all tasks."""
    passed = 0
    total = 0
    for scores in task_scores.values():
        total += 1
        n = len(scores)
        c = sum(1 for s in scores if s >= threshold)
        if n >= k:
            pass_rate = (
                1.0 - math.comb(n - c, k) / math.comb(n, k)
                if n - c >= k
                else 1.0
            )
        else:
            pass_rate = 1.0 if c > 0 else 0.0
        passed += pass_rate
    return passed / total if total > 0 else 0.0


def summarize_job(job_dir: Path) -> dict:
    """Extract key metrics from a Harbor job directory."""
    result_file = job_dir / "result.json"
    if not result_file.exists():
        print(f"ERROR: {result_file} not found", file=sys.stderr)
        sys.exit(1)

    with open(result_file) as f:
        data = json.load(f)

    # Extract config
    config_file = job_dir / "config.json"
    config = {}
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)

    # Collect per-trial rewards and individual metrics grouped by task
    task_scores: dict[str, list[float]] = {}
    task_metrics: dict[str, dict[str, list[float]]] = {}
    all_scores: list[float] = []

    for entry in sorted(os.listdir(job_dir)):
        reward_file = job_dir / entry / "verifier" / "reward.json"
        if not reward_file.is_file():
            continue
        with open(reward_file) as f:
            r = json.load(f)
        task_name = entry.rsplit("__", 1)[0]
        score = r.get("blended_reward", r.get("reward", 0.0))
        task_scores.setdefault(task_name, []).append(score)
        all_scores.append(score)

        # Collect individual metrics across all pages in this trial
        tm = task_metrics.setdefault(task_name, {"ssim": [], "phash": [], "color_hist": [], "height_ratio": []})
        ssim_vals = [v for k, v in r.items() if "ssim_cropped" in k]
        phash_vals = [v for k, v in r.items() if "phash_cropped" in k]
        color_vals = [v for k, v in r.items() if "color_hist_cropped" in k]
        height_vals = [v for k, v in r.items() if "height_ratio" in k]

        if ssim_vals: tm["ssim"].append(sum(ssim_vals) / len(ssim_vals))
        if phash_vals: tm["phash"].append(sum(phash_vals) / len(phash_vals))
        if color_vals: tm["color_hist"].append(sum(color_vals) / len(color_vals))
        if height_vals: tm["height_ratio"].append(sum(height_vals) / len(height_vals))

    if not all_scores:
        print("WARNING: No trial rewards found", file=sys.stderr)
        all_scores = [0.0]

    # Per-task summary with individual metric averages
    per_task = {}
    for task_name, scores in sorted(task_scores.items()):
        mean = sum(scores) / len(scores)
        tm = task_metrics.get(task_name, {})
        per_task[task_name] = {
            "mean": round(mean, 4),
            "min": round(min(scores), 4),
            "max": round(max(scores), 4),
            "n": len(scores),
            "mean_ssim": round(sum(tm["ssim"]) / len(tm["ssim"]), 4) if tm.get("ssim") else 0.0,
            "mean_phash": round(sum(tm["phash"]) / len(tm["phash"]), 4) if tm.get("phash") else 0.0,
            "mean_color_hist": round(sum(tm["color_hist"]) / len(tm["color_hist"]), 4) if tm.get("color_hist") else 0.0,
            "mean_height_ratio": round(sum(tm["height_ratio"]) / len(tm["height_ratio"]), 4) if tm.get("height_ratio") else 0.0,
        }

    stats = data.get("stats", {})
    eval_key = list(stats.get("evals", {}).keys())[0] if stats.get("evals") else ""
    eval_stats = stats.get("evals", {}).get(eval_key, {})

    mean_reward = sum(all_scores) / len(all_scores)
    std_reward = (
        sum((s - mean_reward) ** 2 for s in all_scores) / len(all_scores)
    ) ** 0.5

    return {
        "run_id": job_dir.name,
        "timestamp": data.get("started_at", ""),
        "model": config.get("model", eval_key.split("__")[0] if eval_key else "unknown"),
        "agent": eval_key.split("__")[0] if eval_key else "unknown",
        "env": config.get("env", "unknown"),
        "n_tasks": len(task_scores),
        "n_trials": len(all_scores),
        "n_errors": eval_stats.get("n_errors", 0),
        "mean_reward": round(mean_reward, 4),
        "min_reward": round(min(all_scores), 4),
        "max_reward": round(max(all_scores), 4),
        "std_reward": round(std_reward, 4),
        "pass_at_1_070": round(_compute_pass_at_k(task_scores, 0.70, 1), 4),
        "pass_at_5_070": round(_compute_pass_at_k(task_scores, 0.70, 5), 4),
        "pass_at_10_070": round(_compute_pass_at_k(task_scores, 0.70, 10), 4),
        "per_task_json": json.dumps(per_task),
        "job_path": str(job_dir),
    }, task_scores


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


def append_to_history(summary: dict) -> None:
    """Append to history CSV and save a dedicated job summary JSON."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Append to global history CSV
    file_exists = HISTORY_CSV.exists()
    with open(HISTORY_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(summary)

    # 2. Save dedicated job summary JSON in results/<job_id>/
    job_results_dir = RESULTS_DIR / summary["run_id"]
    job_results_dir.mkdir(parents=True, exist_ok=True)
    
    summary_json_path = job_results_dir / "summary.json"
    # Unpack per_task_json for cleaner reading in the standalone file
    standalone_summary = dict(summary)
    standalone_summary["per_task"] = json.loads(standalone_summary.pop("per_task_json"))
    
    with open(summary_json_path, "w") as f:
        json.dump(standalone_summary, f, indent=2)


def update_evaluation_report(summary: dict, task_scores: dict[str, list[float]]) -> None:
    """Update the tables in docs/evaluation_report.md with fresh numbers."""
    report_path = Path(__file__).resolve().parent.parent / "docs" / "evaluation_report.md"
    if not report_path.exists():
        return

    content = report_path.read_text()

    # 1. Build Aggregate Results Table
    per_task = json.loads(summary["per_task_json"])
    
    archetype_map = {
        "v1-fooddeliveryplayfulmediumconf": "Food Delivery (Playful)",
        "v1-lawfirmcorporateeasyconfig-73": "Law Firm (Corporate Clean)",
        "v1-cryptoexchangecyberpunkhardco": "Crypto Exchange (Cyberpunk)",
        "v1-musicstreaminggradientmediumc": "Music Streaming (Gradient)",
        "v1-wellnessspaorganiceasyconfig": "Wellness Spa (Organic Warm)",
        "v1-aistartupneonhardconfig-73475": "AI Startup (Neon Dark)",
        "v1-indiegameretromediumconfig-73": "Indie Game Studio (Retro)",
        "v1-travelagencytropicalmediumcon": "Travel Agency (Tropical)",
        "v1-architecturestudiomonohardcon": "Architecture Studio (Mono)",
        "v1-luxuryfashionserifmediumconfi": "Luxury Fashion (Serif)",
    }

    table_lines = [
        "<!-- RESULTS_TABLE_START -->",
        "| Archetype | Mean Blended Reward | Min | Max | Std Dev |",
        "| :--- | :---: | :---: | :---: | :---: |"
    ]

    for task_key, stats in sorted(per_task.items(), key=lambda x: -x[1]["mean"]):
        name = archetype_map.get(task_key, task_key.replace("v1-", "").replace("config-73475", ""))
        scores = task_scores[task_key]
        mean = stats["mean"]
        std = (sum((s - mean) ** 2 for s in scores) / len(scores)) ** 0.5
        table_lines.append(f"| **{name}** | **{mean:.3f}** | {stats['min']:.3f} | {stats['max']:.3f} | {std:.3f} |")

    table_lines.append(f"| **Overall Suite Average** | **{summary['mean_reward']:.3f}** | **{summary['min_reward']:.3f}** | **{summary['max_reward']:.3f}** | **{summary['std_reward']:.3f}** |")
    table_lines.append("<!-- RESULTS_TABLE_END -->")

    # Replace RESULTS_TABLE
    start_tag = "<!-- RESULTS_TABLE_START -->"
    end_tag = "<!-- RESULTS_TABLE_END -->"
    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        content = before + "\n".join(table_lines) + after

    # 2. Build Pass@K Table
    pass_lines = [
        "<!-- PASS_AT_K_START -->",
        "| Threshold | Pass@1 | Pass@2 | Pass@5 | Pass@10 |",
        "| :---: | :---: | :---: | :---: | :---: |"
    ]
    
    thresholds = [0.50, 0.60, 0.70, 0.75, 0.80]
    for thresh in thresholds:
        p1 = _compute_pass_at_k(task_scores, thresh, 1)
        p2 = _compute_pass_at_k(task_scores, thresh, 2)
        p5 = _compute_pass_at_k(task_scores, thresh, 5)
        p10 = _compute_pass_at_k(task_scores, thresh, 10)
        pass_lines.append(f"| ≥ {thresh:.2f} | {p1:.0%} | {p2:.0%} | {p5:.0%} | {p10:.0%} |")
    pass_lines.append("<!-- PASS_AT_K_END -->")

    # Replace PASS_AT_K
    p_start_tag = "<!-- PASS_AT_K_START -->"
    p_end_tag = "<!-- PASS_AT_K_END -->"
    if p_start_tag in content and p_end_tag in content:
        before = content.split(p_start_tag)[0]
        after = content.split(p_end_tag)[1]
        content = before + "\n".join(pass_lines) + after

    # 3. Update Plot Paths
    plot_lines = [
        "<!-- PLOTS_START -->",
        f"![Task Variance Boxplot](../results/{summary['run_id']}/task_variance_boxplot.png)",
        "",
        f"![Task Means Barchart](../results/{summary['run_id']}/task_means_barchart.png)",
        "<!-- PLOTS_END -->"
    ]
    
    pl_start_tag = "<!-- PLOTS_START -->"
    pl_end_tag = "<!-- PLOTS_END -->"
    if pl_start_tag in content and pl_end_tag in content:
        before = content.split(pl_start_tag)[0]
        after = content.split(pl_end_tag)[1]
        content = before + "\n".join(plot_lines) + after

    report_path.write_text(content)
    print(f"  Updated docs/evaluation_report.md with latest metrics and plot paths.")


def print_summary(summary: dict) -> None:
    """Print a human-readable summary to stdout."""
    print()
    print("=" * 60)
    print(f"  Evaluation Summary: {summary['run_id']}")
    print("=" * 60)
    print(f"  Model:       {summary['model']}")
    print(f"  Tasks:       {summary['n_tasks']}")
    print(f"  Trials:      {summary['n_trials']} ({summary['n_errors']} errors)")
    print(f"  Mean Reward: {summary['mean_reward']:.4f}")
    print(f"  Range:       [{summary['min_reward']:.4f}, {summary['max_reward']:.4f}]")
    print(f"  Std Dev:     {summary['std_reward']:.4f}")
    print(f"  Pass@1  ≥0.70: {summary['pass_at_1_070']:.1%}")
    print(f"  Pass@5  ≥0.70: {summary['pass_at_5_070']:.1%}")
    print(f"  Pass@10 ≥0.70: {summary['pass_at_10_070']:.1%}")
    print()

    per_task = json.loads(summary["per_task_json"])
    print(f"  {'Task':<50} {'Mean':>7} {'Min':>7} {'Max':>7}")
    print("  " + "─" * 75)
    for task, stats in sorted(per_task.items(), key=lambda x: -x[1]["mean"]):
        short = task.replace("v1-", "").replace("config-73475", "")[:45]
        print(f"  {short:<50} {stats['mean']:>7.4f} {stats['min']:>7.4f} {stats['max']:>7.4f}")

    print()
    print(f"  Results saved to: {HISTORY_CSV}")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize a Harbor job and append to results history."
    )
    parser.add_argument(
        "--job",
        type=str,
        default=None,
        help="Path to the job directory. Defaults to the latest job.",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Print summary only, don't append to history CSV.",
    )
    args = parser.parse_args()

    job_dir = Path(args.job) if args.job else find_latest_job()
    if not job_dir.is_absolute():
        job_dir = Path.cwd() / job_dir

    summary, task_scores = summarize_job(job_dir)
    print_summary(summary)
    update_evaluation_report(summary, task_scores)

    if not args.no_save:
        append_to_history(summary)


if __name__ == "__main__":
    main()
