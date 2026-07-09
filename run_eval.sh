#!/usr/bin/env bash
# run_eval.sh — Thin wrapper around eval/run.py
#
# Prerequisites:
#   uv installed:   curl -LsSf https://astral.sh/uv/install.sh | sh
#   harbor:         uv tool install harbor
#   Docker running (for --env docker configs)
#
# Usage:
#   ./run_eval.sh --config v0_generated
#   ./run_eval.sh --config v0_generated --n-concurrent-trials 10

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v uv &>/dev/null; then
    source "$HOME/.local/bin/env" 2>/dev/null || true
fi

if ! command -v uv &>/dev/null; then
    echo "ERROR: uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

uv --directory "$SCRIPT_DIR" run python -m eval.run "$@"

# Automatically summarize results after the eval completes
echo ""
echo "Summarizing results..."
uv --directory "$SCRIPT_DIR" run python -m eval.summarize

echo ""
echo "Generating visualization plots..."
uv --directory "$SCRIPT_DIR" run --with matplotlib --with seaborn python -m eval.visualize
