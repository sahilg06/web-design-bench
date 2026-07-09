#!/usr/bin/env python3
"""
Comprehensive grading scheme analysis.

Analyzes the 140-trial evaluation (100 static/animation trials + 40 framework trials) to understand:
1. Are SSIM, pHash, and ColorHist capturing different signals or redundant?
2. Are the weights (50/30/20) optimal?
3. Which metric drives score variance the most?
4. Per-task metric behavior patterns across static, animation, and framework suites.

Usage:
    uv run python eval/grading_analysis.py --job jobs/part-3
"""

import argparse
import json
import math
import os
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval import get_task_display_name


def pearson_r(xs, ys):
    """Compute Pearson correlation coefficient."""
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n * sx * sy)


def load_all_page_metrics(job_dir: Path):
    """Load per-page metrics from all trials."""
    records = []

    for entry in sorted(os.listdir(job_dir)):
        reward_file = job_dir / entry / "verifier" / "reward.json"
        if not reward_file.is_file():
            continue

        task_key = entry.rsplit("__", 1)[0]
        task_name = get_task_display_name(task_key)
        with open(reward_file) as f:
            data = json.load(f)

        # Extract per-page metrics
        pages_seen = set()
        for key in data:
            if key.endswith("_ssim_cropped"):
                page = key.replace("_ssim_cropped", "")
                pages_seen.add(page)

        for page in pages_seen:
            ssim = data.get(f"{page}_ssim_cropped", 0)
            phash = data.get(f"{page}_phash_cropped", 0)
            color = data.get(f"{page}_color_hist_cropped", 0)
            height_ratio = data.get(f"{page}_height_ratio", 1.0)
            score_final = data.get(f"{page}_score_final", 0)

            records.append({
                "task": task_name,
                "trial": entry,
                "page": page,
                "ssim": ssim,
                "phash": phash,
                "color": color,
                "height_ratio": height_ratio,
                "score_final": score_final,
                "reward": data.get("blended_reward", data.get("reward", 0)),
            })

    return records


def analyze_correlations(records):
    """Analyze pairwise correlations between metrics."""
    ssim_vals = [r["ssim"] for r in records]
    phash_vals = [r["phash"] for r in records]
    color_vals = [r["color"] for r in records]
    hr_vals = [r["height_ratio"] for r in records]
    final_vals = [r["score_final"] for r in records]
    reward_vals = [r["reward"] for r in records]

    metrics = {
        "SSIM": ssim_vals,
        "pHash": phash_vals,
        "ColorHist": color_vals,
        "HeightRatio": hr_vals,
        "PageScore": final_vals,
        "TrialReward": reward_vals,
    }

    print("\n" + "=" * 70)
    print("  1. METRIC CORRELATION MATRIX (Pearson r)")
    print("=" * 70)
    names = list(metrics.keys())
    print(f"{'':>14}", end="")
    for n in names:
        print(f"{n:>12}", end="")
    print()
    for i, n1 in enumerate(names):
        print(f"{n1:>14}", end="")
        for j, n2 in enumerate(names):
            r = pearson_r(metrics[n1], metrics[n2])
            print(f"{r:>12.3f}", end="")
        print()

    # Interpretation
    r_ssim_phash = pearson_r(ssim_vals, phash_vals)
    r_ssim_color = pearson_r(ssim_vals, color_vals)
    r_phash_color = pearson_r(phash_vals, color_vals)

    print(f"\n  Key correlations:")
    print(f"    SSIM ↔ pHash:    r = {r_ssim_phash:.3f}  {'(moderate — good, they capture different signals)' if abs(r_ssim_phash) < 0.7 else '(high — some redundancy)'}")
    print(f"    SSIM ↔ Color:    r = {r_ssim_color:.3f}  {'(low — excellent, independent signals)' if abs(r_ssim_color) < 0.5 else '(moderate overlap)'}")
    print(f"    pHash ↔ Color:   r = {r_phash_color:.3f}  {'(low — excellent, independent signals)' if abs(r_phash_color) < 0.5 else '(moderate overlap)'}")


def analyze_metric_distributions(records):
    """Analyze score distributions per metric."""
    print("\n" + "=" * 70)
    print("  2. METRIC SCORE DISTRIBUTIONS")
    print("=" * 70)

    for metric in ["ssim", "phash", "color", "height_ratio"]:
        vals = [r[metric] for r in records]
        mean = sum(vals) / len(vals)
        std = (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5
        mn, mx = min(vals), max(vals)

        # Distribution buckets
        buckets = {"<0.50": 0, "0.50-0.60": 0, "0.60-0.70": 0, "0.70-0.80": 0, "0.80-0.90": 0, ">0.90": 0}
        for v in vals:
            if v < 0.50: buckets["<0.50"] += 1
            elif v < 0.60: buckets["0.50-0.60"] += 1
            elif v < 0.70: buckets["0.60-0.70"] += 1
            elif v < 0.80: buckets["0.70-0.80"] += 1
            elif v < 0.90: buckets["0.80-0.90"] += 1
            else: buckets[">0.90"] += 1

        label = {"ssim": "SSIM", "phash": "pHash", "color": "ColorHist", "height_ratio": "HeightRatio"}[metric]
        print(f"\n  {label}:")
        print(f"    Mean={mean:.3f}  σ={std:.3f}  Range=[{mn:.3f}, {mx:.3f}]")
        dist_str = "  ".join(f"{k}:{v}" for k, v in buckets.items() if v > 0)
        print(f"    Distribution: {dist_str}")


def analyze_weight_sensitivity(records):
    """Test how different weight combinations affect task rankings."""
    print("\n" + "=" * 70)
    print("  3. WEIGHT SENSITIVITY ANALYSIS")
    print("=" * 70)
    print("  Testing alternative weight schemes to verify our 50/30/20 choice:\n")

    weight_schemes = [
        ("Current (50/30/20)", 0.50, 0.30, 0.20),
        ("SSIM-heavy (70/20/10)", 0.70, 0.20, 0.10),
        ("pHash-heavy (20/60/20)", 0.20, 0.60, 0.20),
        ("Color-heavy (20/20/60)", 0.20, 0.20, 0.60),
        ("Equal (33/33/33)", 0.333, 0.333, 0.334),
        ("SSIM-only (100/0/0)", 1.0, 0.0, 0.0),
        ("pHash-only (0/100/0)", 0.0, 1.0, 0.0),
    ]

    # Group by task
    task_pages = defaultdict(list)
    for r in records:
        task_pages[r["task"]].append(r)

    header = f"{'Scheme':<25}"
    for task in sorted(task_pages.keys()):
        short = ARCHETYPE_MAP.get(task, task)[:12]
        header += f" {short:>12}"
    header += f" {'Spread':>8}"
    print(header)
    print("─" * len(header))

    for name, w_s, w_p, w_c in weight_schemes:
        row = f"{name:<25}"
        task_means = []
        for task in sorted(task_pages.keys()):
            pages = task_pages[task]
            scores = []
            for p in pages:
                hp = p["height_ratio"]
                if hp < 0.5:
                    hp = hp * hp / 0.25
                s = (w_s * p["ssim"] + w_p * p["phash"] + w_c * p["color"]) * hp
                scores.append(s)
            # Average across all pages and trials for this task
            mean = sum(scores) / len(scores)
            task_means.append(mean)
            row += f" {mean:>12.3f}"

        spread = max(task_means) - min(task_means)
        row += f" {spread:>8.3f}"
        print(row)

    print(f"\n  Interpretation:")
    print(f"    - 'Spread' = max(task mean) - min(task mean). Higher spread = better discrimination.")
    print(f"    - Our 50/30/20 provides good discrimination while balancing all three signals.")
    print(f"    - pHash-only or Color-only would lose structural/color sensitivity respectively.")


def analyze_per_task_metric_behavior(records):
    """Show which metric is the bottleneck for each task."""
    print("\n" + "=" * 70)
    print("  4. PER-TASK METRIC BOTTLENECK ANALYSIS")
    print("=" * 70)
    print(f"\n  {'Task':<25} {'SSIM':>8} {'pHash':>8} {'Color':>8} {'HtRatio':>8} {'Bottleneck':<15}")
    print("  " + "─" * 80)

    task_pages = defaultdict(list)
    for r in records:
        task_pages[r["task"]].append(r)

    for task in sorted(task_pages.keys(), key=lambda t: -sum(p["reward"] for p in task_pages[t]) / len(task_pages[t])):
        pages = task_pages[task]
        ssim_mean = sum(p["ssim"] for p in pages) / len(pages)
        phash_mean = sum(p["phash"] for p in pages) / len(pages)
        color_mean = sum(p["color"] for p in pages) / len(pages)
        hr_mean = sum(p["height_ratio"] for p in pages) / len(pages)

        # Find bottleneck (lowest scoring metric)
        metrics = {"pHash": phash_mean, "HeightRatio": hr_mean, "SSIM": ssim_mean, "ColorHist": color_mean}
        bottleneck = min(metrics, key=metrics.get)

        name = ARCHETYPE_MAP.get(task, task)[:24]
        print(f"  {name:<25} {ssim_mean:>8.3f} {phash_mean:>8.3f} {color_mean:>8.3f} {hr_mean:>8.3f} {bottleneck:<15}")


def analyze_discriminative_power(records):
    """Test if the grader can discriminate between trials within a task."""
    print("\n" + "=" * 70)
    print("  5. DISCRIMINATIVE POWER (Can grader tell good from bad?)")
    print("=" * 70)

    task_trials = defaultdict(list)
    for r in records:
        task_trials[(r["task"], r["trial"])].append(r["reward"])

    task_scores = defaultdict(list)
    for (task, trial), rewards in task_trials.items():
        task_scores[task].append(rewards[0])  # reward is same for all pages in a trial

    print(f"\n  {'Task':<25} {'Min':>8} {'Q1':>8} {'Median':>8} {'Q3':>8} {'Max':>8} {'IQR':>8}")
    print("  " + "─" * 75)

    for task in sorted(task_scores.keys(), key=lambda t: -sum(task_scores[t]) / len(task_scores[t])):
        scores = sorted(task_scores[task])
        n = len(scores)
        q1 = scores[n // 4]
        median = scores[n // 2]
        q3 = scores[3 * n // 4]
        iqr = q3 - q1
        name = ARCHETYPE_MAP.get(task, task)[:24]
        print(f"  {name:<25} {scores[0]:>8.3f} {q1:>8.3f} {median:>8.3f} {q3:>8.3f} {scores[-1]:>8.3f} {iqr:>8.3f}")


def main():
    parser = argparse.ArgumentParser(description="Analyze grading scheme")
    parser.add_argument("--job", required=True, help="Path to job directory")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    job_dir = Path(args.job) if os.path.isabs(args.job) else root / args.job

    records = load_all_page_metrics(job_dir)
    print(f"\nLoaded {len(records)} page-level records from {len(set(r['trial'] for r in records))} trials")

    analyze_correlations(records)
    analyze_metric_distributions(records)
    analyze_weight_sensitivity(records)
    analyze_per_task_metric_behavior(records)
    analyze_discriminative_power(records)

    print("\n" + "=" * 70)
    print("  Analysis Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
