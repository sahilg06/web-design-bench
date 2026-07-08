"""
web-design-bench grader package.

Provides visual similarity scoring, HTML rendering, and text recall
evaluation for comparing AI-generated website reproductions against
reference designs.

Modules:
    grade       — Multi-metric visual similarity scorer (SSIM + pHash + Color Histogram)
    render      — Playwright-based HTML → screenshot renderer
    text_recall — HTML text content recall scorer via token overlap
"""

__version__ = "0.1.0"
