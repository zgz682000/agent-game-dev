

from typing import Literal
from abc import ABC
from typing import override
from core.tools.doc_tool import DocReadTool, DocToolFactory, DocWriteTool
import os
from core.prompts.markdown_tool_prompts import MARKDOWN_WRITE_TOOL_DESCRIPTION, MARKDOWN_READ_TOOL_DESCRIPTION

class MarkdownWriteTool(DocWriteTool, ABC):
    def __init__(
        self, *, 
        approval_mode: Literal["always_require", "never_require"] | None = None,
        folder_path: str = "."
    ):
        super().__init__(name="markdown_write", description=MARKDOWN_WRITE_TOOL_DESCRIPTION, approval_mode=approval_mode)
        self._folder_path = folder_path
    @override
    async def _write_doc(self, doc_name: str, doc_content: str):
        path = os.path.join(self._folder_path, doc_name + ".md")
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(doc_content)
        return path

    
class MarkdownReadTool(DocReadTool, ABC):
    def __init__(self, *, approval_mode: Literal["always_require", "never_require"] | None = None, folder_path: str = "."):
        super().__init__(name="markdown_read", description=MARKDOWN_READ_TOOL_DESCRIPTION, approval_mode=approval_mode)
        self._folder_path = folder_path

    @override
    async def _read_doc(self, doc_name: str)->str:
        with open(os.path.join(self._folder_path, doc_name + ".md"), "r") as f:
            return f.read()

class MarkdownToolFactory(DocToolFactory):
    def __init__(self, *, folder_path: str):
        self._folder_path = folder_path

    @property
    @override
    def doc_format_name(self) -> str:
        return "Markdown"

    @override
    def create_doc_read_tool(self) -> DocReadTool:
        return MarkdownReadTool(folder_path=self._folder_path)

    @override
    def create_doc_write_tool(self) -> DocWriteTool:
        return MarkdownWriteTool(folder_path=self._folder_path)