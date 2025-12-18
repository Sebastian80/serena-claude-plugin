"""Tests for Serena plugin.

These tests require fastapi and toolbus (bridge) to be available.
They are skipped if dependencies are missing.
"""

import pytest

from serena import __version__


def test_package_version():
    """Test package version."""
    assert __version__ == "1.1.0"


# Plugin tests - require bridge dependencies
try:
    from serena import SerenaPlugin
    HAS_BRIDGE_DEPS = True
except ImportError:
    HAS_BRIDGE_DEPS = False


@pytest.mark.skipif(not HAS_BRIDGE_DEPS, reason="Bridge dependencies not available")
def test_plugin_name():
    """Test plugin name property."""
    plugin = SerenaPlugin()
    assert plugin.name == "serena"


@pytest.mark.skipif(not HAS_BRIDGE_DEPS, reason="Bridge dependencies not available")
def test_plugin_version():
    """Test plugin version."""
    plugin = SerenaPlugin()
    assert plugin.version == "1.0.0"


@pytest.mark.skipif(not HAS_BRIDGE_DEPS, reason="Bridge dependencies not available")
def test_plugin_description():
    """Test plugin description."""
    plugin = SerenaPlugin()
    assert "LSP" in plugin.description
