"""Evaluation runner configuration registry."""

_REGISTRY: dict[str, type] = {}


def register_config(name: str):
    """Decorator to register an evaluation config class by name."""
    def decorator(cls):
        _REGISTRY[name] = cls
        return cls
    return decorator


def load_config(name: str):
    """Load a registered config by name. Raises KeyError if not found."""
    if name not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY.keys())) or "(none)"
        raise KeyError(
            f"Config '{name}' not found. Available configs: {available}"
        )
    return _REGISTRY[name]


import os
import re
from pathlib import Path


def get_task_display_name(task_key: str) -> str:
    """
    Dynamically look up the clean display name of a task from its task.toml metadata.
    Handles truncated task keys (e.g., from Harbor logs) and provides robust fallbacks.
    """
    tasks_dir = Path(__file__).resolve().parent.parent / "tasks"
    if tasks_dir.exists():
        for task_dir in tasks_dir.iterdir():
            if task_dir.is_dir() and task_dir.name.startswith(task_key):
                toml_path = task_dir / "task.toml"
                if toml_path.is_file():
                    content = toml_path.read_text(encoding="utf-8", errors="replace")
                    m = re.search(r'display_name\s*=\s*"([^"]+)"', content)
                    if m:
                        return m.group(1)
                    m_arch = re.search(r'archetype\s*=\s*"([^"]+)"', content)
                    m_diff = re.search(r'difficulty\s*=\s*"([^"]+)"', content)
                    if m_arch:
                        arch = m_arch.group(1).replace("_", " ").title()
                        diff = m_diff.group(1).capitalize() if m_diff else "Medium"
                        return f"{arch} ({diff})"

    clean = task_key.replace("v1-", "").replace("v2-", "").replace("v3-", "").replace("config-73475c", "").replace("config-73475", "").replace("config", "")
    return clean.replace("_", " ").title()
