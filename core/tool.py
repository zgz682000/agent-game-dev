from abc import ABC, abstractmethod
from typing import Any, Callable
from agent_framework import ToolProtocol

class Tool(ABC):
    def __init__(self, *, name: str, description: str | None = None, instructions: str | None = None):
        self.name = name
        self.description = description
        self.instructions = instructions

    def __str__(self):
        return f"{self.name}: {self.description}"

    @abstractmethod
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        raise NotImplementedError("Subclasses must implement this method")