"""
Configuration registry for web-design-bench archetypes.

Provides a decorator-based registration system so that archetype configs
can be defined declaratively in library.py and loaded by name at runtime.

Usage:
    from recipe.configs import register_config, load_config

    @register_config("my_archetype")
    class MyConfig(_Base):
        ...

    config = load_config("my_archetype")
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ── Global registry ──────────────────────────────────────────────────────────

_CONFIG_REGISTRY: dict[str, type] = {}


def register_config(name: str):
    """
    Class decorator that registers a GenerationConfig under the given name.

    Raises ValueError if the name is already taken — prevents silent overwrites
    when two configs accidentally share a slug.
    """
    def decorator(cls: type) -> type:
        if name in _CONFIG_REGISTRY:
            raise ValueError(
                f"Config name '{name}' is already registered by "
                f"{_CONFIG_REGISTRY[name].__name__}. Choose a unique slug."
            )
        _CONFIG_REGISTRY[name] = cls
        cls._config_name = name
        logger.debug("Registered config: %s -> %s", name, cls.__name__)
        return cls
    return decorator


def load_config(name: str) -> Any:
    """
    Instantiate a registered GenerationConfig by its slug name.

    Raises ValueError with a helpful message listing available configs
    if the requested name is not found.
    """
    cls = _CONFIG_REGISTRY.get(name)
    if cls is None:
        available = sorted(_CONFIG_REGISTRY.keys())
        raise ValueError(
            f"Unknown config '{name}'. "
            f"Available configs: {available}"
        )
    return cls()


def list_configs() -> list[str]:
    """Return sorted list of all registered config names."""
    return sorted(_CONFIG_REGISTRY.keys())
