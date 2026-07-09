"""Eval runner: launches Harbor eval jobs for a named config.

Usage:
    python -m eval.run --config <config_name>

Examples:
    python -m eval.run --config v0_generated
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Import config modules so their @register_config decorators fire.
import eval.configs  # noqa: F401
from eval import load_config


REPO_ROOT = Path(__file__).parent.parent


def resolve_api_key() -> str:
    """Resolve the Anthropic API key from env var or macOS Keychain."""
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        try:
            result = subprocess.run(
                [
                    "security", "find-generic-password",
                    "-s", "anthropic-api-key",
                    "-a", os.environ.get("USER", ""),
                    "-w",
                ],
                capture_output=True,
                text=True,
            )
            key = result.stdout.strip()
        except Exception:
            pass
    if not key:
        sys.exit(
            "ERROR: ANTHROPIC_API_KEY not set and not found in macOS Keychain.\n"
            "  Store it with: security add-generic-password "
            "-s 'anthropic-api-key' -a \"$USER\" -w '<key>'"
        )
    return key


def harbor_cmd() -> list[str]:
    """Return the harbor invocation, preferring PATH then uv tool run."""
    if shutil.which("harbor"):
        return ["harbor"]
    return ["uv", "tool", "run", "--from", "harbor", "harbor"]


def _run_parallel(config, api_key: str, jobs_dir: Path, extra: list[str]) -> None:
    """Single harbor run --config call with n_concurrent_trials parallelism."""
    n_concurrent = getattr(config, "N_CONCURRENT_TRIALS", 1)
    n_attempts = getattr(config, "N_ATTEMPTS", 1)
    build_timeout_x = getattr(config, "ENV_BUILD_TIMEOUT_MULTIPLIER", None)

    for task_rel_path in config.TASKS:
        if not (REPO_ROOT / task_rel_path).exists():
            sys.exit(f"ERROR: Task path does not exist: {REPO_ROOT / task_rel_path}")

    job_cfg = {
        "jobs_dir": str(jobs_dir),
        "n_concurrent_trials": n_concurrent,
        "n_attempts": n_attempts,
        "environment": {"type": config.ENV},
        "agents": [{"name": config.AGENT, "model": config.MODEL}],
        "tasks": [
            {"path": str(REPO_ROOT / t)} for t in config.TASKS
        ],
    }
    if build_timeout_x is not None:
        job_cfg["environment_build_timeout_multiplier"] = build_timeout_x

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", prefix="harbor_job_", delete=False
    ) as f:
        json.dump(job_cfg, f, indent=2)
        job_cfg_path = f.name

    print(
        f"Running {len(config.TASKS)} tasks "
        f"({n_attempts} attempts each, {n_concurrent} concurrent) via Harbor JobConfig …"
    )
    try:
        cmd = [
            *harbor_cmd(), "run",
            "--config", job_cfg_path,
            "--ae", f"ANTHROPIC_API_KEY={api_key}",
            *extra,
        ]
        subprocess.run(cmd, check=True)
    finally:
        Path(job_cfg_path).unlink(missing_ok=True)


def _run_sequential(config, api_key: str, jobs_dir: Path, extra: list[str]) -> None:
    """Legacy: one harbor run per task, sequentially."""
    n_attempts = getattr(config, "N_ATTEMPTS", 1)
    build_timeout_x = getattr(config, "ENV_BUILD_TIMEOUT_MULTIPLIER", None)
    for task_rel_path in config.TASKS:
        task_path = REPO_ROOT / task_rel_path
        if not task_path.exists():
            sys.exit(f"ERROR: Task path does not exist: {task_path}")

        cmd = [
            *harbor_cmd(), "run",
            "--path", str(task_path),
            "--agent", config.AGENT,
            "--model", config.MODEL,
            "--env", config.ENV,
            "--jobs-dir", str(jobs_dir),
            "--ae", f"ANTHROPIC_API_KEY={api_key}",
            "--n-concurrent", str(config.N_CONCURRENT),
            "--n-attempts", str(n_attempts),
        ]
        if build_timeout_x is not None:
            cmd += ["--environment-build-timeout-multiplier", str(build_timeout_x)]
        cmd += extra
        subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Harbor eval jobs for a named config."
    )
    parser.add_argument("--config", required=True, help="Registered config name")
    parser.add_argument(
        "--n-concurrent-trials", type=int,
        help="Override N_CONCURRENT_TRIALS in config",
    )
    args, extra = parser.parse_known_args()

    config = load_config(args.config)

    if args.n_concurrent_trials is not None:
        config.N_CONCURRENT_TRIALS = args.n_concurrent_trials

    api_key = resolve_api_key()

    jobs_dir = REPO_ROOT / "jobs"
    jobs_dir.mkdir(exist_ok=True)

    if getattr(config, "N_CONCURRENT_TRIALS", None):
        _run_parallel(config, api_key, jobs_dir, extra)
    else:
        _run_sequential(config, api_key, jobs_dir, extra)


if __name__ == "__main__":
    main()
