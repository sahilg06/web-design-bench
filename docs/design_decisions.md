# Design Decisions & Architectural Trade-offs

This document outlines the core research philosophy, engineering decisions, and trade-offs made while architecting `web-design-bench`.

---

## 1. The Grader: Why a 3-Metric Formula?

The problem statement explicitly warns: *"The model will learn your grading logic, so if your grading is bad, you're just introducing noise to the model and making it worse."*

### The Flaw in Pure SSIM / pHash
Many visual web benchmarks evaluate generated pages using image similarity metrics. Design2Code [[3]](#ref-3) decomposes evaluation into element-level sub-metrics (Block-Match, Text, Position, Color) combined with CLIP embeddings, while VisualWebArena [[4]](#ref-4) uses SSIM-based fuzzy image matching for visually grounded task evaluation. In our benchmark, we adopt full-page screenshot comparison using Structural Similarity (SSIM) [[1]](#ref-1) and Perceptual Hashing (pHash) [[2]](#ref-2) — both well-established image quality metrics. While effective for layout geometry, we observed a critical failure mode during early testing: **Color Palette Hallucination**.
* If an agent generates a beautifully aligned SaaS website but uses a **light theme (`#ffffff`)** instead of the requested **dark theme (`#0a0a0f`)**, SSIM and pHash still score the layout surprisingly high (often >0.70) because the structural edges and text bounding boxes match perfectly.
* In a real-world product environment, generating a light theme when a dark theme was requested is a catastrophic failure.

### The Solution: 3D HSV Color Histogram Correlation
To solve this without making the grader brittle to minor pixel shifts, we introduced a third metric: **Color Histogram Correlation (20% weight)**.
```
Visual_Score = 0.50 * SSIM + 0.30 * pHash + 0.20 * ColorHistogramSimilarity
```
* **Mechanism**: We convert both screenshots to the HSV color space and compute a 3D histogram (32 hue bins, 32 saturation bins, 32 value bins). We then compare the histograms using Pearson correlation via OpenCV (`cv2.compareHist`).
* **Result**: If an agent gets the layout right but hallucinates the wrong background or brand colors, the Color Histogram score drops to near 0.0, dragging the overall visual reward down to `<0.60`. This provides a much cleaner gradient for RL alignment.

### Empirical Validation: Metric Independence (from 500 page-level records)

We validated the formula by computing **Pearson correlations** between all metric pairs across 500 page-level measurements (100 trials × 5 pages). The three metrics are remarkably independent:

| Metric Pair | Pearson r | Interpretation |
| :--- | :---: | :--- |
| SSIM ↔ pHash | **-0.055** | Near-zero — completely independent signals |
| SSIM ↔ ColorHist | **0.421** | Weak positive — mostly independent |
| pHash ↔ ColorHist | **-0.139** | Near-zero — independent signals |

This confirms each metric captures a genuinely **different aspect** of design fidelity. If they were correlated (r > 0.8), having three would add no value over one.

### Weight Sensitivity: Why 50/30/20?

We tested 7 weight schemes and measured **Spread** (max task mean - min task mean) as a proxy for discriminative power:

| Scheme | Spread | Verdict |
| :--- | :---: | :--- |
| SSIM-only (100/0/0) | 0.134 | ❌ Cannot discriminate between tasks |
| Current (50/30/20) | 0.203 | ✅ Good balance of discrimination + stability |
| Equal (33/33/33) | 0.224 | ✅ Also viable |
| pHash-only (0/100/0) | 0.356 | ❌ Too volatile — Luxury Fashion drops to 0.41 |

The 50/30/20 split provides good discrimination while keeping scores in the **RL-useful range** (all tasks > 0.50). pHash-heavy schemes create tasks with near-zero RL gradient.

### Per-Task Bottleneck Discovery

| Bottleneck | Tasks Affected | Pattern |
| :--- | :---: | :--- |
| **pHash** | 6/10 tasks | Whitespace-heavy and minimal designs |
| **SSIM** | 4/10 tasks | Designs with complex gradients or precise spacing |
| **ColorHist** | 0/10 tasks | Never the bottleneck — acts as a penalty-only metric |

> Full analysis available via `uv run python eval/grading_analysis.py --job <job_dir>`

---

## 2. Handling Page Height & Truncation

A major challenge in grading full-page website screenshots is handling height mismatches. If the ground-truth reference is `5000px` tall but the agent's generated page is only `2500px` tall (due to omitting the footer and FAQ sections), how do you grade it fairly?

### Cropped vs. Padded Comparison
* **Cropped Mode**: We crop both images to `min(ref_height, gen_height)`. This evaluates the quality of the sections the agent *did* generate, without penalizing them for what's missing.
* **Padded Mode**: We pad the shorter image with background color to `max(ref_height, gen_height)`. This heavily penalizes missing sections because the padded white/black space will mismatch the reference content.

### Our Non-Linear Height Penalty
Rather than forcing a rigid choice between cropped and padded, our grader computes `max(score_cropped, score_padded)` to find the fairest alignment, but then applies a **non-linear height penalty**:
```python
height_ratio = min(ref_h, gen_h) / max(ref_h, gen_h)
if height_ratio < 0.5:
    # Quadratic penalty for severe truncation
    penalty = (height_ratio / 0.5) ** 2
else:
    # Linear penalty for minor differences
    penalty = height_ratio
```
This ensures that minor font-rendering differences (`4900px` vs `5000px`) receive almost no penalty, while severe truncation (`2000px` vs `5000px`) is aggressively punished.

---

## 3. Text Recall Mechanics: Why Recall over Precision/F1?

To catch instances where agents output visually perfect layouts but utilize `Lorem Ipsum` placeholder texts or omit critical textual information, we integrate a semantic token recall check (`mean_text_recall`).

### The Flaw in Precision & F1-Score
In standard NLP tasks, evaluating Precision or F1-score is standard practice. However, in AI coding agent evaluation, we observed that **measuring Precision penalizes positive agent behavior**:
* If an AI agent decides to add *extra* helpful text—such as expanding an FAQ section, adding a descriptive subtitle to a card, or inserting accessibility labels—that is considered high-quality agent behavior.
* If we measured Precision ($|GT \cap Agent| / |Agent|$), the agent would be aggressively penalized for adding this extra high-quality content. By strictly measuring Recall ($|GT \cap Agent| / |GT|$), we ensure the agent covers 100% of the ground truth without punishing it for over-delivering.

### Lorem Ipsum Filtering (`LOREM_RE`)
Before scoring, the verifier checks if the ground-truth reference page *itself* consists of `Lorem Ipsum` placeholder text. If the reference design is just a wireframe template with Latin placeholders, text recall is meaningless. In this case, the script intelligently skips text scoring for that page and defaults to `recall = 1.0` so the agent isn't unfairly penalized.

---

## 4. Execution Infrastructure: Playwright vs. Selenium/Puppeteer

To render agent HTML into full-page screenshots, we selected **Playwright (Async Python API)** over Selenium or Puppeteer.

### Engineering Rationale
a. **Async Concurrency**: Rendering 5 pages across 10 tasks requires 50 browser sessions. Using `asyncio` with Playwright allows us to render multiple pages concurrently within the verifier container, reducing grading overhead by 70% compared to synchronous Selenium.

b. **Network-Idle Guarantees**: A common failure in automated screenshot capture is taking the screenshot before web fonts or external assets finish loading. We utilize `page.goto(url, wait_until="networkidle")` followed by a `500ms` animation settling timeout to ensure the DOM is fully rendered.

c. **Strict Pixel Scaling**: We force `device_scale_factor=1` in the browser context. This guarantees that screenshot dimensions match the reference assets pixel-for-pixel, preventing retina display scaling discrepancies across different execution environments.

---

## 5. Strict No-JS Policy & Safety Validators

To ensure agents are evaluated purely on front-end CSS/HTML design skills rather than programming scripts or event hacks, we enforce a **strict no-JS policy** via `recipe/validators/javascript.py`.

### Trade-offs
* **Limitation**: Without JavaScript, we cannot evaluate interactive components like modal popups, working accordions, or dynamic carousels.
* **Benefit**: It completely eliminates sandbox escape risks, prevents agents from using JavaScript to artificially manipulate the DOM to pass the visual grader, and forces the model to demonstrate pure CSS mastery (e.g., using flexbox/grid for layout, CSS transitions for hover effects).

---

## 6. Recipe Stability: Achieving a Mean CV of 4.8%

The work trial explicitly requires *"a recipe that is stable."* A benchmark is only useful for RL training if repeated runs produce consistent rewards — otherwise, the reward signal degrades into noise and the model cannot learn.

Our recipe achieves a **mean Coefficient of Variation (CV) of 4.8%** across all 10 tasks, with **7/10 tasks under 5% CV** and a **0% error rate** across 100 trials. This stability is the direct result of four deliberate architectural choices:

### a. Deterministic Rendering Environment
Both the ground-truth reference screenshots and the agent's screenshots are rendered inside the **same Dockerfile** — using the same Playwright version (`1.44.0`), the same bundled Chromium, the same `fonts-liberation` package, and the same `device_scale_factor=1`. This eliminates cross-environment rendering drift (font substitution, subpixel antialiasing, retina scaling) that plagues many visual benchmarks.

### b. Multi-Metric Smoothing
By blending three orthogonal metrics (`SSIM`, `pHash`, `ColorHistogram`) across five pages per task, we average out per-page noise. A single page that renders slightly differently contributes only `1/15th` (1 page × 1 metric out of 5 pages × 3 metrics) of the final visual reward, dramatically reducing score volatility.

### c. `max(cropped, padded)` Alignment
Rather than committing to a single comparison mode (which can be unfairly sensitive to minor height differences), we compute both cropped and padded scores and take the maximum. This ensures the grader always finds the fairest geometric alignment, reducing noise from minor font-rendering height variations.

### d. Zero-Crash Verifier Design
By ensuring pure numeric reward schemas (`{"reward": 0.0, "blended_reward": 0.0}`) and installing all system dependencies deterministically in the Dockerfile, we achieved a **0% error rate** — no trial was ever lost to an infrastructure crash, timeout, or dependency mismatch.

> See the full empirical stability breakdown (per-task CV table) in [Evaluation Report → Recipe Stability](evaluation_report.md).

---

## 7. Considered but Rejected & Future Work: Design Principles & Aesthetic Metrics

During the design of the grader, we explored incorporating explicit design principle metrics to evaluate the aesthetic quality of the generated websites.

### Considered but Rejected: Static Heuristic Metrics (Ngo's Aesthetic Measures)
We evaluated traditional mathematical models of aesthetics, such as **Ngo's 14 Aesthetic Measures** ([[6]](#ref-6), [Ngo et al., 2000](https://www.mi.sanu.ac.rs/vismath/ngo/index.html)), which quantify principles like Balance, Equilibrium, Symmetry, Sequence, Proportion, and Regularity using bounding box geometry.

We ultimately chose **not** to include these in the current grader for three reasons:
a. **Replication vs. Absolute Aesthetics**: Our benchmark is fundamentally a *replication fidelity* benchmark. A reference design might intentionally feature asymmetric layouts (e.g., our Architecture Studio) or extreme whitespace (e.g., Luxury Fashion). An absolute symmetry or balance metric would incorrectly penalize faithful replications of intentional asymmetry.

b. **RL Gaming Risks**: Static mathematical formulas are highly susceptible to reward hacking by RL agents. An agent could optimize for Ngo's Symmetry and Balance by outputting a perfectly centered grid of identical grey boxes—scoring perfectly on the heuristic while failing the design brief.

c. **DOM Dependency**: Ngo's formulas require segmenting individual UI objects and calculating their optical weight and coordinates, which would require complex DOM parsing or object detection, making the grader brittle.

### Future Work: Learned Multimodal Evaluation (Design-o-meter)
For future iterations of `web-design-bench` (particularly for open-ended generation tasks where there is no ground-truth screenshot), we plan to move beyond static heuristics to learned, VLM-based design evaluators.

Specifically, we propose integrating **Design-o-meter: Towards Evaluating and Refining Graphic Designs** ([[5]](#ref-5), [Goyal et al., 2024](https://arxiv.org/abs/2411.14959)).
* **Human-Aligned Evaluation**: Unlike rigid geometric formulas, Design-o-meter leverages advanced vision-language modeling to evaluate graphic design principles (alignment, hierarchy, typography, clutter, and visual balance) in a manner that aligns with professional human designers.
* **Iterative Self-Refinement**: Design-o-meter not only scores designs but provides actionable natural language critique and refinement suggestions. In a future pipeline iteration, this could be used both as a dense reward signal for RLHF/RLAIF and as an in-context critique loop for agent self-correction.

---

## 📚 Documentation Navigation

Explore the complete documentation suite to understand the full lifecycle of `web-design-bench`:
1. **[Main README & Quick-Start](../README.md)**: Repository overview, architecture diagrams, and execution instructions.
2. **[Design Decisions & Trade-offs](design_decisions.md)**: Architectural thought process, grader mechanics, and framework integrations.
3. **[Evaluation Report & Model Behavior](evaluation_report.md)**: Comprehensive analysis of the 100-trial benchmark run, `Pass@K` metrics, and deep dives into AI model failure patterns.
4. **[Visual Grader Validation](grader_validation/grader_validation.md)**: Side-by-side reference vs. agent screenshot comparisons proving higher scores = better designs.
5. **[Part 2: Animations & Temporal State Freezing](part2_animations.md)**: Architecture for grading CSS animations via Playwright frame freezing (`t0`, `t500`, `t1200`) and WebM video generation.
6. **[Part 3: Multi-Framework Benchmark Report](part3_frameworks.md)**: Architectural and empirical analysis of the 2×2 framework matrix (React vs. Solid JS, Vanilla vs. Tailwind CSS).

---

## 📖 References & Citations

<a name="ref-1"></a> **[1]** Wang, Z., Bovik, A. C., Sheikh, H. R., & Simoncelli, E. P. (2004). *Image quality assessment: from error visibility to structural similarity*. IEEE Transactions on Image Processing, 13(4), 600-612.

<a name="ref-2"></a> **[2]** Zauner, C. (2010). *Implementation and Benchmarking of Perceptual Image Hash Functions*. Master's thesis, Upper Austria University of Applied Sciences.

<a name="ref-3"></a> **[3]** Cheng, S., et al. (2024). *Design2Code: How Far Are We From Automating Front-End Engineering?* [arXiv:2403.03163](https://arxiv.org/abs/2403.03163).

<a name="ref-4"></a> **[4]** Koh, J. Y., et al. (2024). *VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks*. [arXiv:2401.13649](https://arxiv.org/abs/2401.13649).

<a name="ref-5"></a> **[5]** Goyal, S., et al. (2024). *Design-o-meter: Towards Evaluating and Refining Graphic Designs*. [arXiv:2411.14959](https://arxiv.org/abs/2411.14959).

<a name="ref-6"></a> **[6]** Ngo, D. C. L., et al. (2000). *Aesthetic Measures for Assessing Graphic Screens*. Journal of Information Science and Engineering, 16(1), 97-116.
