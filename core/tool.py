from abc import ABC, abstractmethod
from typing import Any, Callable
from agent_framework import ToolProtocol
from typing import Literal

class Tool(ABC):
    def __init__(self, *, name: str, description: str | None = None, approval_mode: Literal["always_require", "never_require"] | None = None):
        self._name = name
        self._description = description
        self._approval_mode: Literal["always_require", "never_require"] | None = approval_mode
    
    def __str__(self):
        return f"{self._name}: {self._description} (Approval Mode: {self._approval_mode})"

    @abstractmethod
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        raise NotImplementedError("Subclasses must implement this method")