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

    # Collect per-trial rewards grouped by task
    task_scores: dict[str, list[float]] = {}
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

    if not all_scores:
        print("WARNING: No trial rewards found", file=sys.stderr)
        all_scores = [0.0]

    # Per-task summary
    per_task = {}
    for task_name, scores in sorted(task_scores.items()):
        mean = sum(scores) / len(scores)
        per_task[task_name] = {
            "mean": round(mean, 4),
            "min": round(min(scores), 4),
            "max": round(max(scores), 4),
            "n": len(scores),
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
    }


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
    """Append a summary row to the history CSV."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    file_exists = HISTORY_CSV.exists()
    with open(HISTORY_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(summary)


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

    summary = summarize_job(job_dir)
    print_summary(summary)

    if not args.no_save:
        append_to_history(summary)


if __name__ == "__main__":
    main()
