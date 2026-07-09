# 📊 `grader/` — Multivariate Computer Vision & Text Recall Grader

This directory houses the core evaluation engine of `web-design-bench`. Rather than relying on brittle HTML tree-diffing or exact text matching, the framework implements a **multivariate Computer Vision (CV) visual grading pipeline** combined with semantic token recall to score rendered agent implementations against ground-truth designs on a continuous `[0, 1]` scale.

---

## 📂 Directory Layout & File Roles

```markdown
grader/
├── grade.py                # Visual similarity scorer (SSIM + pHash + Color Histogram)
├── render.py               # Playwright screenshot & animation frame renderer
├── text_recall.py          # Semantic token-level content recall scorer
└── test_template/
    └── test.sh             # Shell entry point copied to tasks/tests/test.sh
```

> **Note**: During task packaging (`recipe/packager.py`), `grade.py`, `render.py`, `text_recall.py`, and `test.sh` are copied directly into the `tests/` directory of each generated task. This ensures every Harbor task is completely self-contained and can be verified independently without external dependencies.

---

## 📐 Core Mechanics & Reward Formulas

### 1. Visual Similarity Grader (`grade.py`)
The visual score enforces alignment across three complementary Computer Vision metrics, combined with a quadratic height penalty:

```
Visual Reward (Page) = (0.50 * SSIM_Cropped) + (0.30 * pHash_Score) + (0.20 * Color_Histogram_Correlation)

where pHash_Score = 1.0 - (pHash_Distance / 64.0)
```

* **SSIM (50% weight)**: Highly sensitive to spacing shifts, typography changes, layout grids, alignment breaks, and overflowing boundaries.
* **pHash (30% weight)**: Captures visual gestalt (structural placement of headers, buttons, colors, and balance) regardless of minor sub-pixel rendering deltas.
* **Color Histogram (20% weight)**: Compares 3D HSV color distributions using Pearson correlation. Catches severe color palette mismatches (e.g., agent generating a light theme instead of a dark theme) that SSIM and pHash often underweight.
* **Height Penalty**: Applies a quadratic penalty when the height ratio drops below 0.5, heavily penalizing truncated sections or omitted widgets.

### 2. Semantic Text Recall Grader (`text_recall.py`)
To catch instances where agents output visually perfect layouts but utilize Lorem Ipsum placeholder texts or omit critical textual information, we integrate a semantic token recall check:

```
Text Recall (Page) = |GroundTruth_Tokens intersect Agent_Tokens| / |GroundTruth_Tokens|
```
*Raw HTML text is extracted, normalized, stripped of markup tags, and filtered to remove common stopwords and standard Lorem Ipsum sequences.*

### 3. Holistic Blended Reward
To guide RL agent alignment across both design and content requirements, the verifier blends the visual and text recall scores:

```
Blended Reward = (0.75 * Visual Reward) + (0.25 * Mean Text Recall)
```

---

## ⏱️ Part 2: Animation & Temporal State Freezing

For animation tasks (`v2`), `render.py` utilizes Playwright's `document.getAnimations()` API to pause the CSS animation clock at specific intermediate timestamps (`t0`, `t500`, `t1200`, `t1800`). 

`grade.py` then grades each frozen frame independently against the corresponding reference frozen frame using the exact same 3-metric formula, aggregating them into `animation_score`:

```
animation_score = mean(score_final) across all frozen frame screenshots (t0, t500, t1200, t1800)

Visual Reward (Task) = (0.60 * static_score) + (0.40 * animation_score)
```
