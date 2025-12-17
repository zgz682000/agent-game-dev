from abc import ABC, abstractmethod
from typing import Any, Callable
from agent_framework import ToolProtocol
from typing import Literal

class Tool(ABC):
    def __init__(self, *, name: str, description: str | None = None, approval_mode: Literal["always_require", "never_require"] | None = None):
        self.name = name
        self.description = description
        self.approval_mode: Literal["always_require", "never_require"] | None = approval_mode
    
    def __str__(self):
        return f"{self.name}: {self.description} (Approval Mode: {self.approval_mode})"

    @abstractmethod
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        raise NotImplementedError("Subclasses must implement this method")