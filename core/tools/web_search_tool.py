from abc import ABC, abstractmethod
from core.tool import Tool
from agent_framework import HostedWebSearchTool as AgentFrameworkHostedWebSearchTool
from agent_framework import ToolProtocol, AIFunction
from typing import Callable, Any
from typing import override
from pydantic import BaseModel, Field

class WebSearchTool(Tool, ABC):
    pass


class HostedWebSearchTool(WebSearchTool):
    def __init__(self):
        super().__init__(name="web_search")
        self._tool = AgentFrameworkHostedWebSearchTool()

    @override
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        return self._tool


class ApiBasedWebSearchTool(WebSearchTool):
    class SearchWebInput(BaseModel):
        query: str = Field(description="The query to search the web for")

    def __init__(self):
        super().__init__(name="web_search", approval_mode="never_require")
        self._description = "Search the web for information"

    @abstractmethod
    async def _search_web(self, query: str) -> str:
        pass

    @override
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        return AIFunction(
            name=self._name,
            func=self._search_web,
            input_model=ApiBasedWebSearchTool.SearchWebInput,
            description=self._description,
            approval_mode=self._approval_mode,
        )

    
class WebSearchToolFactory(ABC):
    @abstractmethod
    def create_web_search_tool(self) -> WebSearchTool:
        pass