# `web-design-bench`: Complete Work Trial & Evaluation Submission Summary

> **Submitted by**: Sahil Goyal  
> **Repository**: [https://github.com/sahilg06/web-design-bench](https://github.com/sahilg06/web-design-bench)  
> **Evaluated Target Model**: Claude Code with Opus 4.7 across 180 total trials (Parts 1, 2, & 3)

---

## 🚀 Executive Presentation & Engineering Overview

I designed **`web-design-bench`** as a scalable, production-grade Reinforcement Learning environment recipe built on top of the **Harbor Framework (v1.1)** to rigorously evaluate coding agents across multi-page website replication without sacrificing grading accuracy, multimodal context, or stability.

Rather than relying on brittle HTML tree-diffing, string distance, or scraping existing public websites, I approached this challenge by balancing **scalable synthetic generation**, **uncompromised grading stability**, and **multimodal safety verification**. Every single environment packaged by this pipeline is totally self-contained, completely generated from scratch, and features at least **5 distinct web pages** per site with zero public web crawling.

---

## 🔗 Core Architectural Navigation & Proof of Taste

To demonstrate clear research taste and proactive structural decision-making across all three project deliverables, our documentation breaks down into specialized reports:

| Report Section | Focus Area | Key Highlights & Highlights Link |
| :--- | :--- | :--- |
| **🧠 Architectural Rationale** | **[Design Decisions & Trade-offs](design_decisions.md)** | Explains why we chose continuous Computer Vision alignment over brittle tree-diffing, our Aesthetic LLM generation judges, and strict `No-JS` container safety policies. |
| **📊 Quantitative Ledger** | **[Master Evaluation Report & Model Behavior](evaluation_report.md)** | Contains comprehensive 100-trial and 40-trial quantitative arrays, continuous `[0, 1]` dense distributions, `Pass@K` reliability metrics, and behavioral vulnerability patterns across all 18 tasks. |
| **🔍 Visual Proof** | **[Visual Grader Validation Reports](grader_validation/grader_validation.md)** | Side-by-side composite imagery comparing ground-truth designs against `best` vs. `worst` agent trials across Parts 1, 2, & 3—proving mathematically higher CV rewards explicitly correlate to objectively superior human design quality. |
| **🎬 Animation Mechanics** | **[Part 2: Animations & Temporal Freezing](part2_animations.md)** | Engineering architecture detailing non-lossy CSS animation verification via Playwright browser clock manipulation (`t0`, `t500`, `t1200`) alongside 3-second WebM contextual video rendering. |
| **⚛️ Framework Matrix** | **[Part 3: Multi-Framework SPA Architecture](part3_frameworks.md)** | Technical deep-dive into our 2×2 SPA evaluation space (`React JS vs. Solid JS`, `Vanilla CSS vs. Tailwind CSS`), NodeJS compile-time builds (`npm run build`), and automated headless tab navigation (`#nav-<id>`). |

---

## 🏛️ Comprehensive Deliverables & Findings by Tier

### Part 1: Stable Multi-Page Static RL Environments (`v1`)

* **At-Scale Synthetic Task Generator (`recipe/generate.py`)**: Synthesizes structured, varied 5-page websites across **10 distinct archetypes** spanning corporate law suites, neon AI platforms, dark-mode cyberpunk crypto DEXs, and playful food delivery brands.
* **Continuous Multivariate Visual Grader (`grader/grade.py`)**: Computes a smooth, highly responsive dense reward gradient (`[0, 1]`) right at runtime across structural patterns, macro gestalt, and color distributions without masking sub-pixel shifts:
  $$\text{Visual Reward} = 0.50 \cdot \text{SSIM} + 0.30 \cdot \text{pHash} + 0.20 \cdot \text{ColorHist}$$
  *(Quadratic height ratio degradation heavily penalizes truncated layouts or missed widget sections).*
* **Empirical 100-Trial Performance on Modal**: Running Claude Code with Opus 4.7 across 10 trials per task achieved a **Suite Average of `0.688`** (`0 errors`, `<5%` coefficient of variation across 7 of the 10 tasks).
* **Model Behavioral Learnings**: Claude Code consistently achieves high accuracy across structured, grid-heavy corporate platforms (*Food Delivery `0.775`*, *Law Firm `0.760`*) but exhibits measurable spacing and typography compression on sparse, highly whitespace-dependent layouts (*Architecture Studio `0.606`*).

---

### Part 2: Animations & Temporal State Freezing (`v2`)

* **Solving the "Static Bypass" & Flaky Video Extraction**: Traditional animation grading via lossy video frame extraction suffers heavily from encoding jitter and container CPU flakiness. Moreover, standard static grading allows agents to game rewards by writing static layouts while ignoring animation specifications completely.
* **Our Solution: Playwright Temporal Freezing ([`part2_animations.md`](part2_animations.md))**: We pause the browser's internal rendering clock (`document.getAnimations().forEach(a => { a.currentTime = t_ms; a.pause(); })`) to accurately capture uncompressed PNG structural comparisons right at `t=0ms`, `t=500ms`, `t=1200ms`, and `settled`:
  * **The `t=0ms` Anti-Gaming Guardian**: Checks explicit element hiding (`opacity: 0`). Any agent attempting to bypass animation keyframes triggers an immediate start-state reward penalty right upon execution.
* **Multimodal Context Inclusion**: To empower vision agents to accurately perceive easing duration (`cubic-bezier`), speed, and stagger sequencing, the task pipeline packages high-resolution 3-second **WebM videos** right into the container context (`/app/assets/*.webm`) alongside static reference screenshots.
* **Temporal Insights & "The Uncanny Valley" (`0.717` Suite Mean across 40 Trials)**: While Claude Code reliably implements initial hidden states (`t0=0.775`) and final settled positions (`settled=0.755`), scores dip during mid-flight transitions (`t500=0.729`). This highlights that model reasoning struggles to accurately synchronize multi-stage staggered easing dynamics mid-motion.

---

### Part 3: Multi-Framework Matrix & SPA Verification (`v3`)

* **The 2×2 Matrix Architecture ([`part3_frameworks.md`](part3_frameworks.md))**: Evaluated 4 dedicated Single Page Application combinations directly across component systems and styling paradigms across 40 trials on Modal:
  1. `React JS + Vanilla CSS (`react_css_easy`)` $\rightarrow$ **`0.786` Mean** (`100% Pass@1 ≥0.70`)
  2. `Solid JS + Vanilla CSS (`solid_css_medium`)` $\rightarrow$ **`0.760` Mean** (`90% Pass@1`)
  3. `React JS + Tailwind CSS (`react_tailwind_medium`)` $\rightarrow$ **`0.719` Mean** (`70% Pass@1`)
  4. `Solid JS + Tailwind CSS (`solid_tailwind_hard`)` $\rightarrow$ **`0.711` Mean** (`80% Pass@1`)
* **100% Build & SPA Execution Success (`0 Errors`)**: The headless verifier verifies clean package configuration (`npm run build`), renders compiled bundles (`dist/`), and executes targeted DOM button navigation (`#nav-<tab_id>`) right in-memory via Playwright without page refreshes.
* **Key Research Discovery — "The Tailwind Approximation Gap"**: 
  * **Vanilla CSS (`0.773` average)** substantially outperformed **Tailwind CSS (`0.715` average)** across both component frameworks. Because Tailwind quantizes design parameters into pre-defined scaling intervals (`p-4`, `text-2xl`), agents cannot accurately reproduce fractional screenshot dimensions. Vanilla variables permit sub-pixel micro-tuning (`padding: 18px 24px`), generating measurably higher structural SSIM alignment.
  * **Gradient & Radial Filter Simplification**: On complex dark-mode Tailwind tasks, Claude Code frequently condenses multi-stop glowing backdrop blurs (`filter blur-3xl`) down to simple solid background blocks (`bg-slate-900`), driving noticeable Color Histogram correlation dips.

---

## 🛠️ Instant Verification & Evaluation Automation

The repository is built for clean, immediate execution directly via our wrapper script, automatically collecting trial telemetries and self-synchronizing all quantitative reports across `results/history.csv` and `docs/evaluation_report.md`:

```bash
# Execute jobs cleanly across any specific test suite on Modal or Docker
HARBOR_ENV=modal ./run_eval.sh --config v0_generated    # Part 1 Static
HARBOR_ENV=modal ./run_eval.sh --config v2_animations   # Part 2 Animation Freezes
HARBOR_ENV=modal ./run_eval.sh --config v3_frameworks   # Part 3 Multi-Framework Matrix
```
