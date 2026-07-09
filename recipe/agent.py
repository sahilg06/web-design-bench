"""
Generation agent: runs Claude Code via claude-agent-sdk to produce HTML/CSS.

No Docker or Harbor required — uses the same underlying agent as Harbor eval
but much faster (~2-5 min vs 15+ min with a container).

Flow:
  1. Render the DesignSpec into a generation prompt (via prompt.py)
  2. Run the Claude Code agent in a sandboxed workspace directory
  3. Agent writes style.css + HTML files using its Write tool
  4. Agent calls the custom validate_files tool to self-check
  5. Agent self-corrects until validate_files reports PASSED
  6. recipe/generate.py retrieves files from the workspace (= output_dir)
"""

import os
import re
from pathlib import Path
from typing import Any

import anyio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
    create_sdk_mcp_server,
    query,
    tool,
)

from recipe.prompt import build_prompts

_GEN_DIR = Path(__file__).parent

# ── Regex patterns used by the inline validator ────────────────────────────
_SCRIPT_RE   = re.compile(r"<script[\s>]",              re.IGNORECASE)
_ON_ATTR_RE  = re.compile(r"\bon\w+\s*=",               re.IGNORECASE)
_JS_URI_RE   = re.compile(r'href\s*=\s*["\']javascript:', re.IGNORECASE)
_JS_FILE_RE  = re.compile(r'(src|href)\s*=\s*["\'][^"\']*\.js["\']', re.IGNORECASE)
_CSS_LINK_RE = re.compile(r'<link[^>]+href=["\']style\.css["\']',     re.IGNORECASE)

# ── Module-level slot used to bind the validator to the current run ────────
_run_ctx: dict = {"workspace": None, "pages": [], "framework": "html_css"}


@tool(
    name        = "validate_files",
    description = (
        "Validate the generated website files in the workspace. "
        "Checks that all required files exist and adhere to the requested framework rules "
        "(e.g., pure HTML/CSS forbids JS/scripts; React/Solid requires package.json, vite.config.js, etc.). "
        "Call this after writing all files. Fix errors and call again until PASSED."
    ),
    input_schema = {},
)
async def _validate_files_tool(args: dict[str, Any]) -> dict[str, Any]:
    workspace: Path | None = _run_ctx["workspace"]
    pages: list[dict]      = _run_ctx["pages"]
    fw: str                = _run_ctx.get("framework", "html_css")

    if workspace is None:
        return {"content": [{"type": "text", "text": "ERROR: validator not initialised"}]}

    errors: list[str] = []

    if fw != "html_css":
        # Framework validation (React / Solid JS via Vite)
        required_files = ["package.json", "vite.config.js", "index.html", "src/App.jsx"]
        for fname in required_files:
            if not (workspace / fname).exists():
                errors.append(f"MISSING: {fname}")
        
        # Verify package.json is valid JSON
        pkg_path = workspace / "package.json"
        if pkg_path.exists():
            try:
                json.loads(pkg_path.read_text(encoding="utf-8", errors="replace"))
            except Exception as exc:
                errors.append(f"package.json: invalid JSON — {exc}")

        n = len(required_files)
    else:
        # Pure HTML + CSS validation
        required_html = [p["file"] for p in pages]
        for fname in required_html + ["style.css"]:
            if not (workspace / fname).exists():
                errors.append(f"MISSING: {fname}")

        for fname in required_html:
            fpath = workspace / fname
            if not fpath.exists():
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception as exc:
                errors.append(f"{fname}: cannot read — {exc}")
                continue
            if not _CSS_LINK_RE.search(text):
                errors.append(f"{fname}: missing <link rel='stylesheet' href='style.css'>")
            if _SCRIPT_RE.search(text):
                errors.append(f"{fname}: <script> tag — FORBIDDEN")
            if _ON_ATTR_RE.search(text):
                errors.append(f"{fname}: on* event attribute — FORBIDDEN")
            if _JS_URI_RE.search(text):
                errors.append(f"{fname}: javascript: URI — FORBIDDEN")
            if _JS_FILE_RE.search(text):
                errors.append(f"{fname}: .js file reference — FORBIDDEN")
        n = len(required_html) + 1

    if errors:
        msg = "VALIDATION FAILED — fix these issues and call validate_files again:\n"
        msg += "\n".join(f"  ✗  {e}" for e in errors)
    else:
        msg = f"VALIDATION PASSED ✓  ({n} files OK)"
    return {"content": [{"type": "text", "text": msg}]}



_VALIDATOR_SUFFIX = (
    "\nAfter writing all files, call the validate_files tool "
    "(available as mcp__recipe-validator__validate_files). "
    "Fix any issues it reports, then call it again until it says VALIDATION PASSED. "
    "Do not finish until validation passes."
)


_MCP_SERVER_NAME = "recipe-validator"
_MCP_TOOL_NAME   = f"mcp__{_MCP_SERVER_NAME}__validate_files"


async def _run_agent(spec: dict, workspace: Path, model: str) -> None:
    _run_ctx["workspace"] = workspace
    _run_ctx["pages"]     = spec["pages"]
    _run_ctx["framework"] = spec.get("framework", "html_css")

    mcp_server = create_sdk_mcp_server(_MCP_SERVER_NAME, tools=[_validate_files_tool])

    system_prompt, user_prompt = build_prompts(spec)

    options = ClaudeAgentOptions(
        cwd             = str(workspace),
        permission_mode = "bypassPermissions",
        allowed_tools   = ["Read", "Write", _MCP_TOOL_NAME],
        mcp_servers     = {_MCP_SERVER_NAME: mcp_server},
        system_prompt   = system_prompt + _VALIDATOR_SUFFIX,
        model           = model,
    )

    async for message in query(prompt=user_prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
    print()


def generate_website(
    spec: dict[str, Any],
    output_dir: Path,
    *,
    model: str | None = None,
    max_retries: int = 3,
    max_tokens: int = 16000,
) -> dict[str, str]:
    """
    Run the Claude Code generation agent in a sandboxed workspace.

    The agent writes HTML/CSS directly into output_dir, calls validate_files
    to self-check, and loops until validation passes.

    Returns a dict mapping filename -> content once all required files are present.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    model = model or os.environ.get("GENERATION_MODEL", "claude-opus-4-7")

    print(f"  Generating via claude-agent-sdk ({model}) …")
    anyio.run(_run_agent, spec, output_dir, model)

    fw = spec.get("framework", "html_css")
    if fw != "html_css":
        expected = ["package.json", "vite.config.js", "src/App.jsx"]
    else:
        expected = ["style.css"] + [p["file"] for p in spec["pages"]]
    missing  = [f for f in expected if not (output_dir / f).exists()]
    if missing:
        raise RuntimeError(f"Agent did not produce required files: {missing}")

    print(f"  {len(list(output_dir.iterdir()))} files generated in {output_dir}")

    # Return files dict for compatibility with generate.py expectations
    files = {}
    for f in expected:
        files[f] = (output_dir / f).read_text(encoding="utf-8", errors="replace")
    return files
