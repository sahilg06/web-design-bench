#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# web-design-bench verifier script (test.sh)
#
# Runs inside the Harbor task container as the grading entry point.
# Orchestrates the full evaluation pipeline:
#
#   Step 1: Copy agent output to /logs/artifacts/ (for human review)
#   Step 2: Validate that expected HTML files exist (from pages.json)
#   Step 3: Render agent HTML to full-page screenshots (render.py)
#   Step 4: Grade rendered vs reference screenshots (grade.py)
#   Step 5: Write reward JSON to /logs/verifier/reward.json
#
# Error handling:
#   - If any step fails, a reward of 0.0 is written and the script exits
#     cleanly (exit 0) so Harbor doesn't mark it as a verifier crash.
#   - Individual rendering failures are tolerated (missing pages score 0.0).
#
# Container paths (Harbor convention):
#   /app/output/     — Agent's generated HTML files
#   /app/assets/     — Reference screenshots (page_*_desktop.png)
#   /tests/          — This script + grade.py, render.py, pages.json
#   /logs/verifier/  — Verifier output (reward.json, logs)
#   /logs/artifacts/ — Agent output copy (for human review)
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

VERIFIER_LOG=/logs/verifier
AGENT_OUTPUT=/app/output
REFERENCE_DIR=/app/assets
TESTS_DIR=/tests
SOLUTION_DIR=/app/solution

mkdir -p "$VERIFIER_LOG" /logs/artifacts

echo "=== web-design-bench Verifier ===" | tee "$VERIFIER_LOG/verifier.log"
echo "Started at: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$VERIFIER_LOG/verifier.log"

# ── Helper: write a zero reward and exit cleanly ──────────────────────────────
write_zero_reward() {
    local reason="$1"
    echo "FAIL: $reason" | tee -a "$VERIFIER_LOG/verifier.log"
    echo '{"reward": 0.0, "blended_reward": 0.0}' \
        > "$VERIFIER_LOG/reward.json"
    echo "=== Verifier complete (reward: 0.0) ===" | tee -a "$VERIFIER_LOG/verifier.log"
    exit 0
}

# ── Step 1: Save agent output as artifacts (always, even if incomplete) ───────
echo "" | tee -a "$VERIFIER_LOG/verifier.log"
echo "Step 1: Copying agent output to artifacts..." | tee -a "$VERIFIER_LOG/verifier.log"

if [ -d "$AGENT_OUTPUT" ]; then
    cp -r "$AGENT_OUTPUT"/. /logs/artifacts/ 2>/dev/null || true
    echo "  Copied $(find /logs/artifacts -type f | wc -l | tr -d ' ') files." \
        | tee -a "$VERIFIER_LOG/verifier.log"
else
    echo "  WARNING: Agent output directory not found: $AGENT_OUTPUT" \
        | tee -a "$VERIFIER_LOG/verifier.log"
    write_zero_reward "Agent output directory not found"
fi

# ── Step 2: Validate required files from pages.json ───────────────────────────
echo "" | tee -a "$VERIFIER_LOG/verifier.log"
echo "Step 2: Validating required files..." | tee -a "$VERIFIER_LOG/verifier.log"

if [ ! -f "$TESTS_DIR/pages.json" ]; then
    write_zero_reward "pages.json not found in $TESTS_DIR"
fi

REQUIRED_FILES=$(python3 -c "
import json, sys
try:
    with open('$TESTS_DIR/pages.json') as f:
        d = json.load(f)
    files = [p['file'] for p in d['pages']]
    # Also require style.css if any page references it
    files.append('style.css')
    print('\n'.join(files))
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
") || write_zero_reward "Failed to parse pages.json"

MISSING=0
FOUND=0
while IFS= read -r fname; do
    if [ ! -f "$AGENT_OUTPUT/$fname" ]; then
        echo "  MISSING: $AGENT_OUTPUT/$fname" | tee -a "$VERIFIER_LOG/verifier.log"
        MISSING=$((MISSING + 1))
    else
        echo "  OK: $AGENT_OUTPUT/$fname" | tee -a "$VERIFIER_LOG/verifier.log"
        FOUND=$((FOUND + 1))
    fi
done <<< "$REQUIRED_FILES"

echo "  Summary: $FOUND found, $MISSING missing" | tee -a "$VERIFIER_LOG/verifier.log"

if [ "$MISSING" -gt 0 ]; then
    write_zero_reward "Agent output incomplete: $MISSING file(s) missing"
fi

# ── Step 3: Render agent HTML to screenshots ──────────────────────────────────
RENDERED_DIR="$VERIFIER_LOG/rendered"
echo "" | tee -a "$VERIFIER_LOG/verifier.log"
echo "Step 3: Rendering agent HTML to screenshots..." | tee -a "$VERIFIER_LOG/verifier.log"

python3 "$TESTS_DIR/render.py" \
    --pages-json "$TESTS_DIR/pages.json" \
    --html-dir   "$AGENT_OUTPUT" \
    --output-dir "$RENDERED_DIR" \
    2>&1 | tee -a "$VERIFIER_LOG/verifier.log" \
    || write_zero_reward "Rendering failed"

# Verify that at least one screenshot was produced.
SCREENSHOT_COUNT=$(find "$RENDERED_DIR" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
echo "  Produced $SCREENSHOT_COUNT screenshot(s)." | tee -a "$VERIFIER_LOG/verifier.log"

if [ "$SCREENSHOT_COUNT" -eq 0 ]; then
    write_zero_reward "No screenshots were produced by the renderer"
fi

# ── Step 4: Grade screenshots against references ─────────────────────────────
echo "" | tee -a "$VERIFIER_LOG/verifier.log"
echo "Step 4: Running visual grader..." | tee -a "$VERIFIER_LOG/verifier.log"

# Build grade.py arguments. Include text recall if solution dir exists.
GRADE_ARGS=(
    --pages-json    "$TESTS_DIR/pages.json"
    --reference-dir "$REFERENCE_DIR"
    --rendered-dir  "$RENDERED_DIR"
    --output-json   "$VERIFIER_LOG/reward.json"
)

# If a solution directory exists, enable text recall scoring.
if [ -d "$SOLUTION_DIR" ]; then
    GRADE_ARGS+=(
        --solution-dir "$SOLUTION_DIR"
        --agent-dir    "$AGENT_OUTPUT"
    )
    echo "  Text recall enabled (solution dir found)." | tee -a "$VERIFIER_LOG/verifier.log"
else
    echo "  Text recall disabled (no solution dir)." | tee -a "$VERIFIER_LOG/verifier.log"
fi

python3 "$TESTS_DIR/grade.py" "${GRADE_ARGS[@]}" \
    2>&1 | tee -a "$VERIFIER_LOG/verifier.log" \
    || write_zero_reward "Grading failed"

# ── Step 5: Verify reward.json was written ────────────────────────────────────
echo "" | tee -a "$VERIFIER_LOG/verifier.log"
echo "Step 5: Verifying reward output..." | tee -a "$VERIFIER_LOG/verifier.log"

if [ ! -f "$VERIFIER_LOG/reward.json" ]; then
    write_zero_reward "grade.py did not produce reward.json"
fi

# Validate the JSON is parseable and contains a reward key.
python3 -c "
import json, sys
try:
    with open('$VERIFIER_LOG/reward.json') as f:
        data = json.load(f)
    reward = data.get('blended_reward', data.get('reward', 0.0))
    assert 0.0 <= reward <= 1.0, f'Reward {reward} out of [0, 1] range'
    print(f'  Reward: {reward:.4f}')
except Exception as e:
    print(f'  ERROR validating reward.json: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1 | tee -a "$VERIFIER_LOG/verifier.log" \
    || write_zero_reward "Invalid reward.json format"

echo "" | tee -a "$VERIFIER_LOG/verifier.log"
echo "=== Verifier complete ===" | tee -a "$VERIFIER_LOG/verifier.log"
echo "Final reward.json:" | tee -a "$VERIFIER_LOG/verifier.log"
cat "$VERIFIER_LOG/reward.json" | tee -a "$VERIFIER_LOG/verifier.log"
echo "" | tee -a "$VERIFIER_LOG/verifier.log"
