"""
web-design-bench recipe pipeline.

Generates Harbor framework tasks that evaluate AI agents on replicating
website designs from screenshots using HTML + CSS only.

Pipeline stages:
  1. configs/   — Archetype configuration registry (18 unique website types)
  2. spec.py    — Deterministic DesignSpec builder
  3. prompt.py  — Claude prompt renderer
  4. agent.py   — Claude API website generator
  5. validators/ — JS, structure, and complexity validators
  6. capture.py — Playwright screenshot capture
  7. packager.py — Harbor task directory assembler
  8. generate.py — CLI orchestrator
"""

__version__ = "1.0.0"
