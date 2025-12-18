"""
Serena Plugin Scripts - Bridge compatibility layer.

Re-exports SerenaPlugin from the main serena package.
"""

import sys
from pathlib import Path

# Add the plugin root to sys.path so we can import the serena package
_plugin_root = Path(__file__).parent.parent.parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))

# Re-export plugin class for bridge compatibility
from serena.plugin import SerenaPlugin

__all__ = ["SerenaPlugin"]
