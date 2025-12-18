from abc import ABC, abstractmethod
from typing import Any, Callable
from core.tool import Tool
from agent_framework import ToolProtocol
from agent_framework import AIFunction
from pydantic import BaseModel, Field
from typing import Literal
from typing import override


class DocWriteInput(BaseModel):
    doc_name: str = Field(description="The name of the document")
    doc_content: str = Field(description="The content of the document")

class DocReadInput(BaseModel):
    doc_name: str = Field(description="The name of the document")


class DocReadTool(Tool, ABC):
    def __init__(self, *, name: str, description: str | None = None, approval_mode: Literal["always_require", "never_require"] | None = None):
        super().__init__(name=name, description=description, approval_mode=approval_mode)
    
    @abstractmethod
    async def _read_doc(self, doc_name: str)->str:
        pass

    @override
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        return AIFunction(
            name=self._name,
            func=self._read_doc,
            input_model=DocReadInput,
            approval_mode=self._approval_mode,
            description=self._description or "Read a document",
        )

class DocWriteTool(Tool, ABC):
    def __init__(self, *, name: str, description: str | None = None, approval_mode: Literal["always_require", "never_require"] | None = None):
        super().__init__(name=name, description=description, approval_mode=approval_mode)

    @abstractmethod
    async def _write_doc(self, doc_name: str, doc_content: str) -> Any:
        pass
    
    @override
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        return AIFunction(
            name=self._name,
            func=self._write_doc,
            input_model=DocWriteInput,
            description=self._description or "Write a document",
            approval_mode=self._approval_mode,
        )


class DocToolFactory(ABC):
    
    @property
    @abstractmethod
    def doc_format_name(self) -> str:
        pass

    @abstractmethod
    def create_doc_read_tool(self) -> DocReadTool:
        pass

    @abstractmethod
    def create_doc_write_tool(self) -> DocWriteTool:
        pass