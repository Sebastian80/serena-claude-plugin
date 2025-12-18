"""
Serena Plugin - Semantic code intelligence via LSP.

Thin plugin that uses MCPConnector to auto-discover and expose
Serena's MCP tools. No hand-coded routes needed.
"""

import logging
import os
from typing import Any

from fastapi import APIRouter

from toolbus.connectors import MCPConnector, create_mcp_router

logger = logging.getLogger("serena_plugin")

# Default Serena MCP server URL
DEFAULT_URL = os.environ.get("SERENA_URL", "http://localhost:9121/mcp")


class SerenaPlugin:
    """Serena semantic code navigation plugin.

    Uses MCPConnector to:
    - Auto-discover tools from Serena MCP server
    - Generate routes for all tools
    - Handle session management and health checks
    """

    def __init__(self, bridge_context: dict[str, Any] | None = None) -> None:
        self._connector_registry = None
        self._connector = MCPConnector(
            name="serena",
            url=DEFAULT_URL,
            timeout=120.0,  # LSP operations can be slow
        )
        # Create router immediately - catch-all routes work before/after connect()
        self._router = create_mcp_router(self._connector)

        if bridge_context:
            self._connector_registry = bridge_context.get("connector_registry")

    @property
    def name(self) -> str:
        return "serena"

    @property
    def description(self) -> str:
        return "Semantic code navigation via LSP (PHP)"

    @property
    def version(self) -> str:
        return "2.0.0"

    @property
    def router(self) -> APIRouter:
        """Get router with catch-all MCP proxy routes."""
        return self._router

    @property
    def connector(self) -> MCPConnector:
        return self._connector

    async def startup(self) -> None:
        """Initialize plugin - connect to MCP and discover tools."""
        if self._connector_registry:
            try:
                self._connector_registry.register(self._connector)
                logger.info("Serena: connector registered")
            except ValueError:
                pass  # Already registered

        try:
            await self._connector.connect()
            logger.info(
                f"Serena: connected, {len(self._connector.tools)} tools available"
            )
        except Exception as e:
            logger.warning(f"Serena: connection failed: {e}")

    async def shutdown(self) -> None:
        """Cleanup on shutdown."""
        await self._connector.disconnect()

        if self._connector_registry:
            try:
                self._connector_registry.unregister("serena")
            except Exception:
                pass

        logger.info("Serena: shutdown")

    async def health_check(self) -> dict[str, Any]:
        """Check connection health."""
        status = self._connector.status()
        return {
            "status": "healthy" if status["healthy"] else "unhealthy",
            "circuit_state": status["circuit_state"],
            "failure_count": status.get("failure_count", 0),
            "tools_discovered": status.get("tools_discovered", 0),
        }
