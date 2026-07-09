# 🎬 Part 2: Animations & Temporal State Freezing

This document details the architectural design decisions, grading mechanics, and pipeline extensions implemented to support **Part 2 (Animations)** in `web-design-bench`.

---

## 1. The Challenge of Grading Animations

Evaluating an AI coding agent's ability to replicate web animations (e.g., fade-ins, slide-ups, staggered entrances) introduces two major engineering challenges:
a. **Flaky Video Extraction**: Traditional video-based grading relies on recording mp4/webm videos of the browser and extracting frames. This is highly lossy, CPU-intensive, and prone to severe flakiness due to video encoding artifacts and variable frame rates across container environments.

b. **Reward Hacking (The Static Bypass)**: If an agent is evaluated only on the final settled state of a webpage, it can completely ignore the animation instructions and render a static page—scoring perfectly while failing the prompt.

---

## 2. Our Solution: Temporal State Freezing

To solve these challenges without introducing video encoding noise into the visual grader, `web-design-bench` implements **Temporal State Freezing** using Playwright's `document.getAnimations()` API.

### How It Works
Instead of recording a video for grading, we use Playwright to freeze the browser's animation clock at precise millisecond intervals (`t=0ms`, `t=500ms`, `t=1200ms`), capturing a pristine, uncompressed PNG screenshot at each frozen state.

```javascript
document.getAnimations().forEach(a => {
    a.currentTime = t_ms;
    a.pause();
});
```

### The 3-Stage Frame Evaluation
For every page in an animation task, we capture and evaluate four distinct states:
a. **`t=0ms` (Initial State / Anti-Gaming Guardian)**: Verifies that animated elements start in their correct initial state (e.g., `opacity: 0`, `transform: translateY(30px)`). If an agent attempts the "Static Bypass" by omitting animations, it will fail the `t=0` comparison because the reference screenshot shows the elements hidden/off-screen.

b. **`t=500ms` (Mid-Flight State)**: Evaluates easing curves (`cubic-bezier`), duration, and staggered delays (`animation-delay`).

c. **`t=1200ms` (Near-Settled State)**: Captures the tail end of the animation sequence.

d. **Settled State (`t=2000ms`)**: Evaluates the final static layout fidelity.

---

## 3. WebM Video Recording for Agent Context

While we avoid video for *grading*, vision-equipped agents (like Claude 3.5 Sonnet / Opus) need to see the reference animations in motion to perceive easing, duration, and stagger.

During task generation (`recipe/capture.py`), we use Playwright's built-in `record_video_dir` context option to record a high-resolution **3-second WebM video** for each page/viewport.

### Container Asset Structure (`/app/assets/`)
When an animation task is packaged, the container is populated with both the video and the frozen frames:
```
/app/assets/
├── page_home_desktop.webm       # 3-second video (for agent context)
├── page_home_desktop.png        # Settled state (reference)
├── page_home_desktop_t0.png     # Frozen at T=0ms (grader only)
├── page_home_desktop_t500.png   # Frozen at T=500ms (grader only)
└── page_home_desktop_t1200.png  # Frozen at T=1200ms (grader only)
```

> **Important**: The `instruction.md` only tells the agent to read the `.png` (settled) and `.webm` (video) files. The frozen frame PNGs (`_t0`, `_t500`, `_t1200`) are present in the container but are **not referenced** in the agent's instructions — they exist solely for the grader to compare against. This is by design: the agent must infer animation behavior from the video, not pixel-copy frozen frames.

---

## 4. Reward Formula & Weighting

Each frozen frame screenshot is compared against its corresponding reference frame using our existing 3-metric formula (`0.50 * SSIM + 0.30 * pHash + 0.20 * ColorHist`).

The final visual reward blends the static settled score with the temporal animation score:
```
static_score    = mean(score_final) across all settled screenshots
animation_score = mean(score_final) across all frozen frame screenshots (t0, t500, t1200)

visual_reward   = 0.60 * static_score + 0.40 * animation_score
blended_reward  = 0.75 * visual_reward + 0.25 * mean_text_recall
```

---

## 5. New Animation Archetypes

We added four dedicated animation configs to `recipe/configs/library.py` to benchmark motion design capabilities across different difficulty tiers and temporal mechanics:

### 1. Portfolio Animation (`portfolio_animation_medium`)
* **Brand**: Studio Lumina (*"Living design through motion"*)
* **Visual Style**: Elegant Minimal (Dark theme `#0f0f12`, coral accent `#ff5533`)
* **Motion Specs**: Staggered project card fade-ins (`animation-delay: 0.1s` to `0.6s`), sliding text overlays, pulsing typography numbers, and smooth `cubic-bezier(0.16, 1, 0.3, 1)` easing.

### 2. SaaS Animation (`saas_animation_hard`)
* **Brand**: FlowSync (*"Automate your workflow at the speed of thought"*)
* **Visual Style**: Modern Tech (Clean white `#ffffff`, bright blue `#3b82f6`)
* **Motion Specs**: Sophisticated page entrances (`@keyframes slideInLeft`, `slideInRight`, `fadeInUp`), live metrics counter simulation, infinite client logo scroll, and snappy `cubic-bezier(0.22, 1, 0.36, 1)` motion.

### 3. Creative Agency Animation (`agency_animation_medium`)
* **Brand**: Prism Studio (*"Where ideas take shape"*)
* **Visual Style**: Bold Gradient (Dark theme `#0a0a0f`, purple-to-pink accents `#a855f7`)
* **Motion Specs**: Slow `1.5s`–`2.5s` animations with large stagger delays (`0.3s`–`1.0s`) designed to create distinct visual separation between intermediate frames (`t500` vs `t1200`).

### 4. Fintech Dashboard Animation (`fintech_animation_hard`)
* **Brand**: Vault (*"Your wealth, engineered"*)
* **Visual Style**: Dark Precision (Ultra-dark `#09090b`, emerald green accent `#10b981`)
* **Motion Specs**: Complex multi-phase keyframes (fade → slide → glow pulse) with an extended `t1800` capture point to evaluate micro-animation states and slow stagger choreography.

---

## 6. Generating & Running Animation Tasks

To generate the new animation tasks using your Anthropic API key, run:
```bash
export ANTHROPIC_API_KEY="your-api-key"
python -m recipe.generate --config portfolio_animation_medium
python -m recipe.generate --config saas_animation_hard
python -m recipe.generate --config agency_animation_medium
python -m recipe.generate --config fintech_animation_hard
```

The generated tasks will be prefixed with `v2-` (e.g., `v2-portfolioanimationmediumconfig-73475c`) to distinguish them from Part 1 static tasks (`v1-`).

To evaluate the animation tasks:
```bash
# Via Modal (recommended)
HARBOR_ENV=modal python -m eval.run --config v2_animations

# Or locally with Docker
python -m eval.run --config v2_animations
```

The generated tasks will automatically include the WebM videos, frozen frames, and updated `pages.json` configuration for the verifier.

---

## 7. Grader Validation: Best vs. Worst Animation Trials

To verify that the temporal grader correctly penalizes animation failures, we compared the best and worst trials for `saas_animation_hard`.

#### ✅ SaaS Animation — Best Trial
The agent successfully implemented the `@keyframes` entrances and correct easing curves, maintaining high alignment across all frozen frames (`t0`, `t500`, `t1200`).

![SaaS Animation Best Trial](grader_validation/comparisons/v2-saasanimationhardconfig-73475__best.png)

#### ❌ SaaS Animation — Worst Trial
The agent failed to include the initial hidden states (`opacity: 0`), triggering the anti-gaming penalty at `t=0ms` and causing severe layout mismatches during mid-flight.

![SaaS Animation Worst Trial](grader_validation/comparisons/v2-saasanimationhardconfig-73475__worst.png)

---

## 📚 Documentation Navigation

Explore the complete documentation suite to understand the full lifecycle of `web-design-bench`:
1. **[Main README & Quick-Start](../README.md)**: Repository overview, architecture diagrams, and execution instructions.
2. **[Design Decisions & Trade-offs](design_decisions.md)**: Architectural thought process, grader mechanics, and framework integrations.
3. **[Evaluation Report & Model Behavior](evaluation_report.md)**: Comprehensive analysis of the 100-trial benchmark run, `Pass@K` metrics, and deep dives into AI model failure patterns.
4. **[Visual Grader Validation](grader_validation/grader_validation.md)**: Side-by-side reference vs. agent screenshot comparisons proving higher scores = better designs.
5. **[Part 2: Animations & Temporal State Freezing](part2_animations.md)**: Architecture for grading CSS animations via Playwright frame freezing (`t0`, `t500`, `t1200`) and WebM video generation.
6. **[Part 3: Multi-Framework Benchmark Report](part3_frameworks.md)**: Architectural and empirical analysis of the 2×2 framework matrix (React vs. Solid JS, Vanilla vs. Tailwind CSS).

