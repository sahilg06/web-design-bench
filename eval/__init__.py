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
