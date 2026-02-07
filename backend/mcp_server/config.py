"""
Configuration for the MCP Server
"""
import os
from typing import Optional


class MCPConfig:
    """Configuration class for MCP server settings."""

    def __init__(self):
        # Server settings
        self.host: str = os.getenv("MCP_HOST", "localhost")
        self.port: int = int(os.getenv("MCP_PORT", "8001"))
        self.debug: bool = os.getenv("MCP_DEBUG", "false").lower() == "true"

        # Database settings
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")

        # Tool settings
        self.max_tool_calls_per_request: int = int(os.getenv("MAX_TOOL_CALLS_PER_REQUEST", "10"))
        self.tool_timeout_seconds: int = int(os.getenv("TOOL_TIMEOUT_SECONDS", "30"))

    def get_database_url(self) -> str:
        """Get the database URL."""
        return self.database_url

    def get_host(self) -> str:
        """Get the server host."""
        return self.host

    def get_port(self) -> int:
        """Get the server port."""
        return self.port

    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug

    def get_max_tool_calls(self) -> int:
        """Get maximum number of tool calls per request."""
        return self.max_tool_calls_per_request

    def get_tool_timeout(self) -> int:
        """Get tool timeout in seconds."""
        return self.tool_timeout_seconds


# Global config instance
config = MCPConfig()