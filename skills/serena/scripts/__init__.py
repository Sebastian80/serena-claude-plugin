"""
Serena Plugin Scripts - Bridge compatibility layer.

This module re-exports from the main serena package for backwards
compatibility with the bridge's plugin discovery mechanism.
"""

import sys
from pathlib import Path

# Add the plugin root to sys.path so we can import the serena package
_plugin_root = Path(__file__).parent.parent.parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))

# Re-export plugin class for bridge compatibility
from serena.plugin import SerenaPlugin
from serena.connector import SerenaConnector
from serena.response import success_response, error_response
from serena.deps import serena

__all__ = ["SerenaPlugin", "SerenaConnector", "success_response", "error_response", "serena"]
