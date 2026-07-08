"""
Validation suite for generated websites.

Three validators run in sequence:
  1. javascript.py  — Hard reject: any JS means the site is unusable
  2. structure.py   — Structural: files exist, HTML parses, style.css linked
  3. complexity.py  — Soft check: DOM/CSS metrics vs. difficulty tier bounds
"""
