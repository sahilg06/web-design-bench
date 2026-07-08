# Design Decisions & Architectural Trade-offs

This document outlines the core research philosophy, engineering decisions, and trade-offs made while architecting `web-design-bench`.

---

## 1. The Grader: Why a 3-Metric Formula?

The problem statement explicitly warns: *"The model will learn your grading logic, so if your grading is bad, you're just introducing noise to the model and making it worse."*

### The Flaw in Pure SSIM / pHash
Many existing benchmarks rely on a combination of Structural Similarity (SSIM) and Perceptual Hashing (pHash). While effective for layout geometry, we observed a critical failure mode during early testing: **Color Palette Hallucination**.
* If an agent generates a beautifully aligned SaaS website but uses a **light theme (`#ffffff`)** instead of the requested **dark theme (`#0a0a0f`)**, SSIM and pHash still score the layout surprisingly high (often >0.70) because the structural edges and text bounding boxes match perfectly.
* In a real-world product environment, generating a light theme when a dark theme was requested is a catastrophic failure.

### The Solution: 3D HSV Color Histogram Correlation
To solve this without making the grader brittle to minor pixel shifts, we introduced a third metric: **Color Histogram Correlation (20% weight)**.
```
Visual_Score = 0.50 * SSIM + 0.30 * pHash + 0.20 * ColorHistogramSimilarity
```
* **Mechanism**: We convert both screenshots to the HSV color space and compute a 3D histogram (32 hue bins, 32 saturation bins, 32 value bins). We then compare the histograms using Pearson correlation via OpenCV (`cv2.compareHist`).
* **Result**: If an agent gets the layout right but hallucinates the wrong background or brand colors, the Color Histogram score drops to near 0.0, dragging the overall visual reward down to `<0.60`. This provides a much cleaner gradient for RL alignment.

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

## 3. Strict No-JS Policy & Safety Validators

To ensure agents are evaluated purely on front-end CSS/HTML design skills rather than programming scripts or event hacks, we enforce a **strict no-JS policy** via `recipe/validators/javascript.py`.

### Trade-offs
* **Limitation**: Without JavaScript, we cannot evaluate interactive components like modal popups, working accordions, or dynamic carousels.
* **Benefit**: It completely eliminates sandbox escape risks, prevents agents from using JavaScript to artificially manipulate the DOM to pass the visual grader, and forces the model to demonstrate pure CSS mastery (e.g., using flexbox/grid for layout, CSS transitions for hover effects).

---

## 4. Flat vs. Versioned Directory Structure

Unlike some implementations that split the recipe into `v0/`, `v1/`, `v2/` subdirectories from day one, `web-design-bench` utilizes a **clean, flat structure** (`recipe/`, `grader/`, `eval/`).

### Why?
1. **Single Source of Truth**: By keeping `grader/` as a top-level shared module, we avoid duplicating grading scripts across dozens of task folders. When Harbor packages a task, it dynamically copies the latest clean grader into `tasks/<id>/tests/`.
2. **Maintainability**: A flat structure is significantly easier to debug and extend. If animation grading (Part 2) or multi-framework SPAs (Part 3) are added later, they can cleanly inherit from the base classes in `recipe/` without duplicating the entire generation pipeline.
