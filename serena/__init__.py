"""
Serena - Semantic code intelligence via LSP for AI agents.

Provides symbol search, references, refactoring, cross-session memory,
and project onboarding for 30+ programming languages.
"""

__version__ = "1.1.0"


def __getattr__(name: str):
    """Lazy imports for optional dependencies (fastapi for plugin)."""
    if name == "SerenaConnector":
        from .connector import SerenaConnector
        return SerenaConnector
    if name == "SerenaPlugin":
        from .plugin import SerenaPlugin
        return SerenaPlugin
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["SerenaConnector", "SerenaPlugin", "__version__"]
