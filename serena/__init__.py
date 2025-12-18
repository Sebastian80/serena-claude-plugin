"""
Serena - Semantic code intelligence via LSP for AI agents.

Thin plugin that auto-discovers and exposes Serena MCP tools via the bridge.
"""

__version__ = "2.0.0"


def __getattr__(name: str):
    """Lazy import for SerenaPlugin (requires fastapi/bridge deps)."""
    if name == "SerenaPlugin":
        from .plugin import SerenaPlugin
        return SerenaPlugin
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["SerenaPlugin", "__version__"]
