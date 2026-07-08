#!/usr/bin/env python3
"""
Text content recall scorer for web-design-bench.

Evaluates whether the AI agent reproduced the visible text content from the
reference design. This catches cases where the visual layout looks roughly
correct but the agent used placeholder text (e.g., "Lorem ipsum") instead of
the actual content, or omitted entire sections of text.

Methodology:
    1. Parse both reference and agent HTML using BeautifulSoup.
    2. Strip non-visible elements (<script>, <style>, <noscript>, <svg>, <head>).
    3. Extract the remaining visible text.
    4. Tokenize into words, normalize (lowercase, strip punctuation).
    5. Filter out common English stopwords and single-character tokens
       (these add noise and inflate recall without conveying real content).
    6. Filter out Lorem Ipsum patterns — if the reference page itself uses
       Lorem Ipsum, we return recall=1.0 since there's no meaningful content
       to reproduce.
    7. Compute recall = |GT_tokens ∩ Agent_tokens| / |GT_tokens|.

Why recall instead of F1 or precision?
    - We care most that the agent reproduced ALL the content from the reference.
    - Extra text in the agent output (e.g., additional explanations) is acceptable
      and should not be penalized, hence precision is not measured.

Design note:
    - Tokens shorter than 2 characters are dropped because they're typically
      noise (bullet chars, initials) that aren't meaningful content.
    - Numbers-only tokens are dropped because they're often dynamic/generated.
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Stopwords ──────────────────────────────────────────────────────────────────
# Common English function words that don't carry content-specific meaning.
# Kept intentionally broad — we want recall to focus on domain-relevant words
# like "pricing", "dashboard", "analytics", not "the" and "and".
STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "for", "on", "with",
    "at", "by", "from", "as", "be", "was", "are", "has", "it", "this", "that",
    "we", "our", "you", "your", "us", "its", "not", "but", "so", "if", "all",
    "more", "also", "can", "will", "do", "get", "have", "into", "than", "then",
    "no", "up", "out", "about", "what", "how", "when", "who", "which", "their",
    "they", "them", "been", "any", "per", "via", "new", "use", "may", "just",
    "each", "only", "other", "some", "such", "very", "one", "two", "would",
    "there", "here", "these", "those", "over", "under", "between",
})

# Regex to detect Lorem Ipsum placeholder text.
# If the reference page is itself Lorem Ipsum, text recall is meaningless.
LOREM_RE = re.compile(
    r"\blorem\b|\bipsum\b|\bdolor\b|\bsit\s+amet\b|\bconsectetur\b|\badipiscing\b",
    re.IGNORECASE,
)

# ── Elements to strip ─────────────────────────────────────────────────────────
# These tags contain text that is not visually rendered on the page.
INVISIBLE_TAGS = ["script", "style", "noscript", "svg", "head", "template"]


def extract_visible_text(html_content: str) -> str:
    """
    Extract human-visible text from an HTML document.

    Args:
        html_content: Raw HTML string.

    Returns:
        A single string of all visible text, with tags stripped and
        whitespace normalized.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove elements whose text content is not visually rendered.
    for tag in soup(INVISIBLE_TAGS):
        tag.decompose()

    # get_text with separator=" " avoids concatenating text from adjacent
    # elements (e.g., <span>Hello</span><span>World</span> → "Hello World").
    return soup.get_text(separator=" ")


def tokenize_and_normalize(text: str) -> set[str]:
    """
    Convert raw text into a normalized set of content tokens.

    Steps:
        1. Find all word-like sequences (alphanumeric + currency/percent symbols).
        2. Strip non-alphanumeric characters and lowercase.
        3. Discard tokens that are: too short (< 2 chars), pure digits, or stopwords.

    Args:
        text: Raw visible text string.

    Returns:
        A set of normalized content tokens.
    """
    # Match word-like runs, including tokens with embedded currency/percent symbols.
    raw_tokens = re.findall(r"[a-zA-Z0-9$€£¥%+\-]+", text)

    result: set[str] = set()
    for token in raw_tokens:
        cleaned = re.sub(r"[^a-zA-Z0-9]", "", token).lower()
        if (
            len(cleaned) > 1
            and cleaned not in STOPWORDS
            and not cleaned.isdigit()
        ):
            result.add(cleaned)

    return result


def extract_text_tokens(html_content: str) -> set[str]:
    """
    Full pipeline: HTML → visible text → normalized token set.

    If the content is detected as Lorem Ipsum placeholder, returns an empty
    set so that recall defaults to 1.0 (no meaningful content to measure).

    Args:
        html_content: Raw HTML string.

    Returns:
        Set of normalized content tokens, or empty set if Lorem Ipsum detected.
    """
    visible_text = extract_visible_text(html_content)

    # If the reference itself is Lorem Ipsum, there's no real content to
    # evaluate, so we signal "no ground truth" by returning empty.
    if LOREM_RE.search(visible_text):
        logger.info("Lorem Ipsum detected — skipping text recall for this page.")
        return set()

    return tokenize_and_normalize(visible_text)


def compute_text_recall(
    gt_tokens: set[str],
    agent_tokens: set[str],
) -> float:
    """
    Compute recall of ground-truth tokens in the agent's output.

    recall = |GT ∩ Agent| / |GT|

    Special cases:
        - If GT is empty (e.g., Lorem Ipsum page), recall = 1.0
          (nothing meaningful to reproduce, so the agent is not penalized).
        - If agent tokens are empty but GT is not, recall = 0.0.

    Args:
        gt_tokens:    Normalized token set from the reference HTML.
        agent_tokens: Normalized token set from the agent's HTML.

    Returns:
        Recall score in [0.0, 1.0].
    """
    if not gt_tokens:
        return 1.0
    if not agent_tokens:
        return 0.0
    return len(gt_tokens & agent_tokens) / len(gt_tokens)


def score_page_text_recall(
    reference_html_path: Path,
    agent_html_path: Path,
) -> dict[str, float | int]:
    """
    Compute text recall for a single page.

    Args:
        reference_html_path: Path to the ground-truth HTML file.
        agent_html_path:     Path to the agent's HTML file.

    Returns:
        Dict with keys: recall, gt_token_count, agent_token_count, overlap_count.
    """
    gt_tokens: set[str] = set()
    agent_tokens: set[str] = set()

    if reference_html_path.exists():
        gt_html = reference_html_path.read_text(errors="ignore")
        gt_tokens = extract_text_tokens(gt_html)
    else:
        logger.warning("Reference HTML not found: %s", reference_html_path)

    if agent_html_path.exists():
        agent_html = agent_html_path.read_text(errors="ignore")
        agent_tokens = extract_text_tokens(agent_html)
    else:
        logger.warning("Agent HTML not found: %s", agent_html_path)

    recall = compute_text_recall(gt_tokens, agent_tokens)
    overlap = len(gt_tokens & agent_tokens) if gt_tokens and agent_tokens else 0

    return {
        "recall": round(recall, 4),
        "gt_token_count": len(gt_tokens),
        "agent_token_count": len(agent_tokens),
        "overlap_count": overlap,
    }


def score_all_pages(
    pages_json: Path,
    solution_dir: Path,
    agent_dir: Path,
) -> dict:
    """
    Compute text recall for all pages defined in pages.json.

    Args:
        pages_json:   Path to pages.json configuration.
        solution_dir: Directory containing the reference/solution HTML files.
        agent_dir:    Directory containing the agent's output HTML files.

    Returns:
        Dict with per-page recall scores and a mean_text_recall aggregate.
    """
    with open(pages_json) as f:
        cfg = json.load(f)

    results: dict = {}
    recalls: list[float] = []

    for page_cfg in cfg["pages"]:
        page_name = page_cfg["name"]
        html_file = page_cfg["file"]

        ref_path = solution_dir / html_file
        agent_path = agent_dir / html_file

        page_result = score_page_text_recall(ref_path, agent_path)
        results[page_name] = page_result
        recalls.append(page_result["recall"])

        logger.info(
            "  %s: recall=%.4f (GT=%d, Agent=%d, Overlap=%d)",
            page_name,
            page_result["recall"],
            page_result["gt_token_count"],
            page_result["agent_token_count"],
            page_result["overlap_count"],
        )

    mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
    results["mean_text_recall"] = round(mean_recall, 4)

    logger.info("Mean text recall: %.4f", mean_recall)
    return results


def main() -> int:
    """CLI entry point for standalone text recall scoring."""
    parser = argparse.ArgumentParser(
        description="Compute text content recall between reference and agent HTML."
    )
    parser.add_argument(
        "--pages-json", required=True,
        help="Path to pages.json configuration file",
    )
    parser.add_argument(
        "--solution-dir", required=True,
        help="Directory containing reference/solution HTML files",
    )
    parser.add_argument(
        "--agent-dir", required=True,
        help="Directory containing the agent's output HTML files",
    )
    parser.add_argument(
        "--output-json", default=None,
        help="Optional path to write detailed results JSON",
    )
    args = parser.parse_args()

    results = score_all_pages(
        pages_json=Path(args.pages_json),
        solution_dir=Path(args.solution_dir),
        agent_dir=Path(args.agent_dir),
    )

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(results, indent=2))
        logger.info("Results written to %s", out_path)

    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
