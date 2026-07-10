# 📈 `eval/` — Evaluation Orchestration & Post-Processing

This directory manages the mass-parallel execution of benchmark tasks on Modal and Docker, as well as the post-processing scripts for summarization, statistical visualization, and visual grader validation.

---

## 📂 Directory Layout & File Roles

```markdown
eval/
├── run.py                  # CLI orchestrator for launching Harbor evaluation jobs
├── summarize.py            # Parses job results, generates summary.json, & updates evaluation_report.md
├── visualize.py            # Generates statistical plots (box plots, bar charts) in results/
├── grader_validation.py    # Auto-generates side-by-side reference vs agent comparison images
├── grading_analysis.py     # Advanced statistical sensitivity & bottleneck analysis
└── configs/                # Version-controlled evaluation test suites
    ├── __init__.py         # Defines `v0_generated` (Static) and `v2_animations` (Animation) suites
    └── ...
```

---

## 🚀 CLI Usage & Workflows

### 1. Launch a Mass-Parallel Evaluation Job
To execute an evaluation suite across 100 parallel trials on Modal (10 trials per task):
```bash
# Run Part 1 Static Benchmark (v0_generated)
HARBOR_ENV=modal uv run python -m eval.run --config v0_generated

# Run Part 2 Animation Benchmark (v2_animations)
HARBOR_ENV=modal uv run python -m eval.run --config v2_animations
```
*Raw execution outputs (agent trajectories, verifier logs, reward details) are saved to `jobs/<timestamp>/`.*

### 2. Summarize Results & Generate Plots
Once a job completes, generate `summary.json`, create statistical plots (`task_variance_boxplot.png`, `task_means_barchart.png`), and automatically update `docs/evaluation_report.md`:
```bash
uv run python -m eval.summarize --job jobs/part-1
uv run python -m eval.visualize --job jobs/part-1
```
*Processed summaries and plots are saved to `results/<same-timestamp>/`.*

### 3. Generate Side-by-Side Grader Validation Images
To prove that higher reward scores correspond to better human-perceived designs, generate side-by-side composite images of the best and worst trials for each task:
```bash
uv run python -m eval.grader_validation --job jobs/part-1
```
*Composite images are saved to `docs/grader_validation/comparisons/` and embedded in `docs/grader_validation/grader_validation.md`.*

### 4. Run Advanced Grading Sensitivity Analysis
To analyze metric independence (Pearson correlation between SSIM, pHash, and Color Hist) and identify primary scoring bottlenecks:
```bash
uv run python -m eval.grading_analysis --job jobs/part-1
```
