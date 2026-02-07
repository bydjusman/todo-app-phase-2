from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseMCPTool(ABC):
    """
    Abstract base class for MCP tools.
    All MCP tools should inherit from this class.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the tool."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Return the description of the tool."""
        pass

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Return the parameters schema for the tool."""
        pass

    @abstractmethod
    async def run(self, **kwargs) -> Any:
        """Execute the tool with the given parameters."""
        pass