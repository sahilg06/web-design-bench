#!/usr/bin/env python3
"""
Visual similarity grader for web-design-bench.

Compares rendered screenshots of AI-generated HTML against reference screenshots
using a weighted combination of three complementary image similarity metrics.

Grading Formula:
    Visual_Score = 0.50 * SSIM + 0.30 * pHash + 0.20 * ColorHistogramSimilarity

Why three metrics instead of two?
    - SSIM (Structural Similarity Index): Captures fine-grained pixel-level and
      structural differences — padding, spacing, font rendering, alignment errors.
      It's the gold standard for perceptual quality but is sensitive to small
      geometric shifts. Weight: 0.50 (dominant because it best correlates with
      human perception of layout fidelity).

    - pHash (Perceptual Hash): Captures overall gestalt/composition similarity.
      Robust to minor color/brightness changes and small spatial shifts. It
      answers: "Does this look like the same page at a glance?" Weight: 0.30
      (secondary because it's less sensitive to detail errors but catches
      gross layout mismatches).

    - Color Histogram Similarity: Catches palette/color scheme errors that SSIM
      and pHash may underweight. If the agent uses a light theme when the reference
      is dark, SSIM may still be moderate (structures match) and pHash may be high
      (layout similar), but the color distribution will be drastically different.
      Weight: 0.20 (supplementary metric targeted at color-scheme fidelity).

Height handling:
    Two scoring modes are computed for each page:

    - 'cropped': Both images are cropped to the shorter page's height. This
      evaluates only the overlapping content area, ignoring truncation. Useful
      as a "best-case" quality signal.

    - 'padded': The shorter image is white-padded to match the taller image's
      height. This penalizes the agent for missing below-the-fold content or
      adding excessive whitespace. Used as the primary scoring mode.

    A height_ratio penalty further discounts the score when the page heights
    differ significantly, preventing a short page from scoring high just because
    its visible content area matches well.

Final per-page score:
    page_score = max(score_cropped, score_padded) * height_penalty

    We take the max because the padded mode can be overly harsh for small
    height differences (white padding creates SSIM artifacts), while cropped
    mode ignores truncation. The height_penalty ensures truncation is still
    penalized through a separate, more calibrated mechanism.

Blended reward (with text recall):
    blended_reward = 0.75 * visual_reward + 0.25 * mean_text_recall

Container paths (Harbor convention):
    - Reference screenshots: /app/assets/page_*_desktop.png
    - Agent HTML output:     /app/output/
    - Rendered screenshots:  /logs/verifier/rendered/
    - Reward output:         /logs/verifier/reward.json
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import cv2
import imagehash
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────

# pHash produces a 64-bit hash; max Hamming distance is 64.
PHASH_BITS = 64.0

# Default metric weights (can be overridden via pages.json).
DEFAULT_SSIM_WEIGHT = 0.50
DEFAULT_PHASH_WEIGHT = 0.30
DEFAULT_COLOR_HIST_WEIGHT = 0.20

# Default blended-reward weights (visual vs text recall).
DEFAULT_VISUAL_BLEND_WEIGHT = 0.75
DEFAULT_TEXT_BLEND_WEIGHT = 0.25

# Height ratio below which we start applying an extra penalty.
# If height_ratio < 0.5, the pages are drastically different in length.
HEIGHT_PENALTY_THRESHOLD = 0.5


# ── Image helpers ──────────────────────────────────────────────────────────────

def load_image(path: Path) -> Image.Image:
    """Load an image as RGB PIL Image."""
    return Image.open(path).convert("RGB")


def crop_to_height(img: Image.Image, h: int) -> Image.Image:
    """Crop image to the given height from the top."""
    return img.crop((0, 0, img.width, min(h, img.height)))


def pad_to_height(img: Image.Image, h: int) -> Image.Image:
    """
    Pad image with white pixels at the bottom to reach height h.

    White padding simulates "missing content" — if the agent's page is
    shorter than the reference, the padded region will differ from the
    reference content, naturally penalizing the visual score.
    """
    if img.height >= h:
        return img
    padded = Image.new("RGB", (img.width, h), (255, 255, 255))
    padded.paste(img, (0, 0))
    return padded


def ensure_same_width(img1: Image.Image, img2: Image.Image) -> tuple[Image.Image, Image.Image]:
    """
    Resize both images to the same width if they differ.

    This can happen if the agent rendered at a different viewport width.
    We resize to the reference width to ensure pixel-level comparison is valid.
    """
    if img1.width == img2.width:
        return img1, img2
    target_w = img1.width  # Reference width is authoritative
    if img2.width != target_w:
        scale = target_w / img2.width
        new_h = int(img2.height * scale)
        img2 = img2.resize((target_w, new_h), Image.LANCZOS)
    return img1, img2


def pil_to_numpy(img: Image.Image) -> np.ndarray:
    """Convert PIL Image to float64 numpy array normalized to [0, 1]."""
    return np.array(img, dtype=np.float64) / 255.0


# ── Metric functions ───────────────────────────────────────────────────────────

def compute_ssim(img1: Image.Image, img2: Image.Image) -> float:
    """
    Compute mean SSIM across RGB channels.

    SSIM is computed per-channel and averaged because it was originally designed
    for grayscale images. Per-channel averaging is standard practice and avoids
    color space conversion artifacts.

    Args:
        img1, img2: Same-size RGB PIL Images.

    Returns:
        SSIM score in [0.0, 1.0].
    """
    a1 = pil_to_numpy(img1)
    a2 = pil_to_numpy(img2)

    # Compute SSIM independently for each color channel.
    channel_scores = [
        ssim(a1[:, :, c], a2[:, :, c], data_range=1.0)
        for c in range(3)
    ]
    return float(np.clip(np.mean(channel_scores), 0.0, 1.0))


def compute_phash_similarity(img1: Image.Image, img2: Image.Image) -> float:
    """
    Compute perceptual hash similarity.

    Uses the imagehash library's pHash (DCT-based perceptual hash).
    Converts the Hamming distance to a similarity score in [0, 1]:
        similarity = 1 - (hamming_distance / 64)

    pHash is particularly good at catching gross layout differences
    (e.g., completely wrong page structure) while being tolerant of
    minor rendering differences (anti-aliasing, font substitution).

    Args:
        img1, img2: RGB PIL Images (need not be same size).

    Returns:
        Perceptual hash similarity in [0.0, 1.0].
    """
    h1 = imagehash.phash(img1)
    h2 = imagehash.phash(img2)
    distance = h1 - h2  # Hamming distance
    return float(np.clip(1.0 - distance / PHASH_BITS, 0.0, 1.0))


def compute_color_histogram_similarity(
    img1: Image.Image,
    img2: Image.Image,
    bins: int = 64,
) -> float:
    """
    Compare color distributions using histogram correlation.

    This metric catches cases where the structural layout is similar but
    the color palette is wrong (e.g., dark theme vs light theme, wrong brand
    colors). SSIM and pHash can miss these because they focus on structure
    and edges rather than absolute color values.

    Method:
        1. Convert both images to HSV color space (separates color from
           brightness, making the comparison more perceptually meaningful).
        2. Compute a 3D color histogram (H, S, V channels).
        3. Normalize histograms to probability distributions.
        4. Compare using OpenCV's correlation method (Pearson correlation),
           which returns values in [-1, 1]. We clamp to [0, 1].

    Why HSV instead of RGB?
        HSV separates hue (color identity) from saturation and value
        (brightness). This means two images with the same colors but
        different brightness levels will still show high similarity,
        which is desirable since brightness can vary with rendering.

    Args:
        img1, img2: RGB PIL Images.
        bins: Number of histogram bins per channel (default 64 balances
              sensitivity with noise tolerance).

    Returns:
        Color histogram similarity in [0.0, 1.0].
    """
    # Convert PIL images to OpenCV BGR format, then to HSV.
    arr1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2HSV)
    arr2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2HSV)

    # Compute 3D histograms over H, S, V channels.
    # H range: [0, 180] in OpenCV, S and V: [0, 256].
    hist1 = cv2.calcHist(
        [arr1], [0, 1, 2], None,
        [bins, bins, bins],
        [0, 180, 0, 256, 0, 256],
    )
    hist2 = cv2.calcHist(
        [arr2], [0, 1, 2], None,
        [bins, bins, bins],
        [0, 180, 0, 256, 0, 256],
    )

    # Normalize to probability distributions.
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)

    # Correlation ranges from -1 (inverse) to 1 (identical).
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return float(np.clip(correlation, 0.0, 1.0))


def compute_height_penalty(ref_height: int, gen_height: int) -> float:
    """
    Compute a penalty factor based on page height mismatch.

    A large height difference signals the agent either:
    - Truncated the page (missing content sections), or
    - Added excessive extra content/whitespace.

    The penalty is the ratio min(h1, h2) / max(h1, h2), which equals 1.0
    when heights match and approaches 0.0 for extreme mismatches.

    An additional harsh penalty is applied when the ratio drops below 0.5
    (the page is less than half the expected height), because at that point
    major content sections are certainly missing.

    Args:
        ref_height:  Reference image height in pixels.
        gen_height:  Generated image height in pixels.

    Returns:
        Penalty factor in [0.0, 1.0].
    """
    if max(ref_height, gen_height) == 0:
        return 1.0

    ratio = min(ref_height, gen_height) / max(ref_height, gen_height)

    # Apply extra quadratic penalty for very large mismatches.
    if ratio < HEIGHT_PENALTY_THRESHOLD:
        ratio = ratio * (ratio / HEIGHT_PENALTY_THRESHOLD)

    return float(np.clip(ratio, 0.0, 1.0))


# ── Per-page grading ───────────────────────────────────────────────────────────

def grade_page(
    ref_path: Path,
    gen_path: Path,
    ssim_w: float = DEFAULT_SSIM_WEIGHT,
    phash_w: float = DEFAULT_PHASH_WEIGHT,
    color_hist_w: float = DEFAULT_COLOR_HIST_WEIGHT,
) -> dict[str, float]:
    """
    Grade a single page by comparing reference and generated screenshots.

    Computes metrics in both 'cropped' (overlap area only) and 'padded'
    (penalize truncation) modes, then combines with height penalty.

    Args:
        ref_path:     Path to reference screenshot PNG.
        gen_path:     Path to generated/rendered screenshot PNG.
        ssim_w:       Weight for SSIM in the visual score formula.
        phash_w:      Weight for pHash in the visual score formula.
        color_hist_w: Weight for color histogram in the visual score formula.

    Returns:
        Dict with all individual metrics and composite scores.
    """
    empty_result = {
        "ssim_cropped": 0.0, "phash_cropped": 0.0, "color_hist_cropped": 0.0,
        "ssim_padded": 0.0, "phash_padded": 0.0, "color_hist_padded": 0.0,
        "height_ratio": 0.0, "height_penalty": 0.0,
        "score_cropped": 0.0, "score_padded": 0.0, "score_final": 0.0,
    }

    if not ref_path.exists():
        logger.warning("Reference screenshot not found: %s", ref_path)
        return empty_result
    if not gen_path.exists():
        logger.warning("Generated screenshot not found: %s", gen_path)
        return empty_result

    ref = load_image(ref_path)
    gen = load_image(gen_path)

    # Ensure same width for pixel-level comparison.
    ref, gen = ensure_same_width(ref, gen)

    ref_h, gen_h = ref.height, gen.height
    height_ratio = min(ref_h, gen_h) / max(ref_h, gen_h) if max(ref_h, gen_h) > 0 else 1.0
    height_penalty = compute_height_penalty(ref_h, gen_h)

    # ── Cropped mode: compare only the overlapping top region ──────────────
    crop_h = min(ref_h, gen_h)
    ref_cropped = crop_to_height(ref, crop_h)
    gen_cropped = crop_to_height(gen, crop_h)

    ssim_c = compute_ssim(ref_cropped, gen_cropped)
    phash_c = compute_phash_similarity(ref_cropped, gen_cropped)
    chist_c = compute_color_histogram_similarity(ref_cropped, gen_cropped)

    score_cropped = float(np.clip(
        ssim_w * ssim_c + phash_w * phash_c + color_hist_w * chist_c,
        0.0, 1.0,
    ))

    # ── Padded mode: pad shorter image to match taller ─────────────────────
    pad_h = max(ref_h, gen_h)
    ref_padded = pad_to_height(ref, pad_h)
    gen_padded = pad_to_height(gen, pad_h)

    ssim_p = compute_ssim(ref_padded, gen_padded)
    phash_p = compute_phash_similarity(ref_padded, gen_padded)
    chist_p = compute_color_histogram_similarity(ref_padded, gen_padded)

    score_padded = float(np.clip(
        ssim_w * ssim_p + phash_w * phash_p + color_hist_w * chist_p,
        0.0, 1.0,
    ))

    # ── Final score: best mode × height penalty ───────────────────────────
    # We take the max of cropped and padded because:
    #   - Cropped: measures quality of content that IS present
    #   - Padded:  measures quality accounting for missing content
    # The height_penalty separately handles the truncation punishment,
    # so we don't double-penalize via the padded mode.
    score_final = float(np.clip(
        max(score_cropped, score_padded) * height_penalty,
        0.0, 1.0,
    ))

    return {
        "ssim_cropped": round(ssim_c, 4),
        "phash_cropped": round(phash_c, 4),
        "color_hist_cropped": round(chist_c, 4),
        "ssim_padded": round(ssim_p, 4),
        "phash_padded": round(phash_p, 4),
        "color_hist_padded": round(chist_p, 4),
        "height_ratio": round(height_ratio, 4),
        "height_penalty": round(height_penalty, 4),
        "score_cropped": round(score_cropped, 4),
        "score_padded": round(score_padded, 4),
        "score_final": round(score_final, 4),
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    """
    CLI entry point for the visual grader.

    Reads pages.json for page list, viewport config, and optional weight
    overrides. Computes per-page visual scores and aggregates into a single
    reward value. Optionally computes text recall and blends it in.

    Output: Writes reward dict to --output-json with per-page breakdowns
    and aggregate reward.
    """
    parser = argparse.ArgumentParser(
        description="Visual similarity grader for web-design-bench."
    )
    parser.add_argument(
        "--pages-json", required=True,
        help="Path to pages.json configuration",
    )
    parser.add_argument(
        "--reference-dir", required=True,
        help="Directory containing reference PNG screenshots",
    )
    parser.add_argument(
        "--rendered-dir", required=True,
        help="Directory containing rendered agent PNG screenshots",
    )
    parser.add_argument(
        "--output-json", required=True,
        help="Path to write the reward JSON output",
    )
    parser.add_argument(
        "--solution-dir", default=None,
        help="Path to solution HTML dir (for text recall scoring)",
    )
    parser.add_argument(
        "--agent-dir", default=None,
        help="Path to agent output HTML dir (for text recall scoring)",
    )
    parser.add_argument(
        "--visual-weight", type=float, default=None,
        help="Override visual weight in blended reward (default from pages.json or 0.75)",
    )
    parser.add_argument(
        "--text-weight", type=float, default=None,
        help="Override text weight in blended reward (default from pages.json or 0.25)",
    )
    args = parser.parse_args()

    # ── Load configuration ─────────────────────────────────────────────────
    with open(args.pages_json) as f:
        cfg: dict[str, Any] = json.load(f)

    ref_dir = Path(args.reference_dir)
    gen_dir = Path(args.rendered_dir)
    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Visual metric weights (from pages.json or defaults).
    visual_weights = cfg.get("visual_weights", {})
    ssim_w = cfg.get("ssim_weight", visual_weights.get("ssim", DEFAULT_SSIM_WEIGHT))
    phash_w = cfg.get("phash_weight", visual_weights.get("phash", DEFAULT_PHASH_WEIGHT))
    color_hist_w = cfg.get("color_hist_weight", visual_weights.get("color_hist", DEFAULT_COLOR_HIST_WEIGHT))

    # Blended reward weights.
    blended_cfg = cfg.get("blended_weights", {})
    visual_blend_w = args.visual_weight or blended_cfg.get("visual", DEFAULT_VISUAL_BLEND_WEIGHT)
    text_blend_w = args.text_weight or blended_cfg.get("text_recall", DEFAULT_TEXT_BLEND_WEIGHT)

    fmt = cfg.get("screenshot_fmt", "png")
    active_viewports = cfg.get("active_viewports", list(cfg.get("viewports", {}).keys()))
    animation_frames_ms = cfg.get("animation_frames_ms", None)
    static_weight = cfg.get("static_weight", 0.6)
    animation_weight = cfg.get("animation_weight", 0.4)

    # Text recall setup.
    solution_dir = Path(args.solution_dir) if args.solution_dir else None
    agent_dir = Path(args.agent_dir) if args.agent_dir else None
    compute_text = solution_dir is not None and agent_dir is not None

    logger.info(
        "Visual weights: SSIM=%.2f, pHash=%.2f, ColorHist=%.2f",
        ssim_w, phash_w, color_hist_w,
    )
    logger.info(
        "Blended weights: Visual=%.2f, Text=%.2f",
        visual_blend_w, text_blend_w,
    )
    if animation_frames_ms:
        logger.info(
            "Animation grading enabled: frames=%s, static_weight=%.2f, animation_weight=%.2f",
            animation_frames_ms, static_weight, animation_weight,
        )

    # ── Grade each page × viewport ────────────────────────────────────────
    rewards: dict[str, Any] = {}
    static_scores: list[float] = []
    animation_scores: list[float] = []
    text_recalls: list[float] = []

    for page_cfg in cfg["pages"]:
        page_name = page_cfg["name"]
        page_file = page_cfg.get("file", "")

        for vp in active_viewports:
            key = f"{page_name}_{vp}"
            ref_img = ref_dir / f"{key}.{fmt}"
            gen_img = gen_dir / f"{key}.{fmt}"

            result = grade_page(ref_img, gen_img, ssim_w, phash_w, color_hist_w)

            # Store all per-metric breakdowns for debugging / analysis.
            for metric, value in result.items():
                rewards[f"{key}_{metric}"] = value

            static_scores.append(result["score_final"])

            logger.info(
                "  %s (settled): final=%.4f  (ssim_c=%.4f phash_c=%.4f chist_c=%.4f  "
                "ssim_p=%.4f phash_p=%.4f chist_p=%.4f  h_ratio=%.4f h_pen=%.4f)",
                key,
                result["score_final"],
                result["ssim_cropped"], result["phash_cropped"], result["color_hist_cropped"],
                result["ssim_padded"], result["phash_padded"], result["color_hist_padded"],
                result["height_ratio"], result["height_penalty"],
            )

            # ── Animation frames grading ───────────────────────────────────
            if animation_frames_ms:
                for t_ms in animation_frames_ms:
                    frame_key = f"{key}_t{t_ms}"
                    ref_frame = ref_dir / f"{frame_key}.{fmt}"
                    gen_frame = gen_dir / f"{frame_key}.{fmt}"

                    frame_result = grade_page(ref_frame, gen_frame, ssim_w, phash_w, color_hist_w)
                    for metric, value in frame_result.items():
                        rewards[f"{frame_key}_{metric}"] = value

                    animation_scores.append(frame_result["score_final"])
                    logger.info("    %s: final=%.4f", frame_key, frame_result["score_final"])

            # ── Text recall (once per page, on the first viewport) ─────────
            if compute_text and vp == active_viewports[0]:
                from grader.text_recall import score_page_text_recall
                tr_result = score_page_text_recall(
                    solution_dir / page_file,
                    agent_dir / page_file,
                )
                recall = tr_result["recall"]
                rewards[f"{page_name}_text_recall"] = recall
                text_recalls.append(recall)
                logger.info("  %s: text_recall=%.4f", page_name, recall)

    # ── Aggregate scores ──────────────────────────────────────────────────
    mean_static = round(float(np.mean(static_scores)) if static_scores else 0.0, 4)
    rewards["static_score"] = mean_static

    if animation_frames_ms and animation_scores:
        mean_anim = round(float(np.mean(animation_scores)), 4)
        rewards["animation_score"] = mean_anim
        visual_reward = round(static_weight * mean_static + animation_weight * mean_anim, 4)
        logger.info("Static score: %.4f, Animation score: %.4f -> Visual reward: %.4f", mean_static, mean_anim, visual_reward)
    else:
        visual_reward = mean_static

    rewards["reward"] = visual_reward

    if compute_text and text_recalls:
        mean_tr = round(float(np.mean(text_recalls)), 4)
        blended = round(
            visual_blend_w * visual_reward + text_blend_w * mean_tr, 4
        )
        rewards["mean_text_recall"] = mean_tr
        rewards["blended_reward"] = blended
        logger.info("Text recall (mean): %.4f", mean_tr)
        logger.info(
            "Blended reward: %.4f  (visual=%.4f × %.2f + text=%.4f × %.2f)",
            blended, visual_reward, visual_blend_w, mean_tr, text_blend_w,
        )
    else:
        # When text recall isn't computed, blended_reward = visual_reward.
        rewards["blended_reward"] = visual_reward

    # ── Write output ──────────────────────────────────────────────────────
    out_path.write_text(json.dumps(rewards))

    # Also write a pretty-printed version for human inspection.
    details_path = out_path.parent / "reward_details.json"
    details_path.write_text(json.dumps(rewards, indent=2))

    logger.info("Visual reward (mean final): %.4f", visual_reward)
    logger.info("Reward JSON written to %s", out_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
