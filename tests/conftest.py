"""Pytest configuration and fixtures for Serena tests."""

import pytest


@pytest.fixture
def mock_serena_response():
    """Mock Serena MCP server response."""
    return {
        "status": "ok",
        "result": []
    }
