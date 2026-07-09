# 📚 `docs/` — Structured Documentation & Research Reports

This directory contains the comprehensive documentation suite, architectural thought processes, empirical evaluation reports, and visual grader validation studies for `web-design-bench`.

---

## 📂 Documentation Navigation

```markdown
docs/
├── design_decisions.md     # Architectural thought process, trade-offs, & grader mechanics
├── evaluation_report.md    # Empirical results, Pass@K, stability (CV), & model failure modes
├── part2_animations.md     # Part 2 architecture: temporal state freezing & WebM generation
├── part3_frameworks.md     # Part 3 architecture: 2×2 framework matrix (React/Solid, Vanilla/Tailwind)
└── grader_validation/
    ├── grader_validation.md # Master index for visual validation reports
    ├── grader_validation_part-1.md # Part 1 static benchmark validation report (v1)
    ├── grader_validation_part-3.md # Part 3 framework benchmark validation report (v3)
    └── comparisons/        # Auto-generated side-by-side reference vs agent composite images
```

---

## 📄 Overview of Reports

### 1. [Design Decisions & Trade-offs](design_decisions.md)
* **Purpose**: Details the rigorous engineering thought process behind the benchmark.
* **Key Topics**: Why we chose Computer Vision over HTML tree-diffing, the mathematical defense of our 3-metric formula (`SSIM` + `pHash` + `Color Hist`), the quadratic height penalty, and the No-JS policy.

### 2. [Evaluation Report & Model Behavior](evaluation_report.md)
* **Purpose**: Synthesizes the results of our 100-trial static benchmark, 40-trial animation benchmark, and 40-trial multi-framework benchmark on Modal using Claude Code (Opus 4.7).
* **Key Topics**: Aggregate reward tables, `Pass@K` analysis, benchmark stability (`CV = 4.8%`), Claude Code's strengths/weaknesses, the *Whitespace Paradox*, Part 2 temporal animation trajectories, and Part 3 framework insights.

### 3. [Part 2: Animations & Temporal State Freezing](part2_animations.md)
* **Purpose**: Explains the technical architecture for benchmarking dynamic CSS animations.
* **Key Topics**: How we use Playwright's `document.getAnimations()` to freeze the animation clock at `t0`, `t500`, `t1200`, and `t1800`, how we generate 3-second WebM videos for vision-equipped agents, and how we keep frozen frames isolated for the grader.

### 4. [Part 3: Multi-Framework Benchmark Report & Architectural Analysis](part3_frameworks.md)
* **Purpose**: Provides a comprehensive analysis of agent performance across different component frameworks and styling paradigms.
* **Key Topics**: The 2×2 matrix evaluating React JS vs. Solid JS and Vanilla CSS vs. Tailwind CSS, the *Tailwind Approximation Gap*, Solid JS signal adherence, and quadrant chart performance breakdowns.

### 5. [Visual Grader Validation Reports](grader_validation/grader_validation.md)
* **Purpose**: Provides undeniable visual evidence that our reward function aligns with human aesthetic judgment.
* **Key Topics**: Side-by-side composite comparisons of the best and worst trials for showcase tasks across static (`part-1`), animation (`part-2`), and framework (`part-3`) suites, proving that high scores (`>0.75`) reflect stunning replications while low scores (`<0.60`) exhibit severe truncation and broken whitespace.
