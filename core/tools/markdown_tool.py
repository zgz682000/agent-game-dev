

from typing import Literal
from abc import ABC
from typing import override
from core.tools.doc_tool import DocReadTool, DocToolFactory, DocWriteTool
import os
class MarkdownWriteTool(DocWriteTool, ABC):
    def __init__(
        self, *, 
        approval_mode: Literal["always_require", "never_require"] | None = None,
        folder_path: str = "."
    ):
        super().__init__(name="markdown_write", description="Write a markdown file", approval_mode=approval_mode)
        self.folder_path = folder_path
    @override
    async def write_doc(self, doc_name: str, doc_content: str):
        with open(os.path.join(self.folder_path, doc_name + ".md"), "w") as f:
            f.write(doc_content)

    
class MarkdownReadTool(DocReadTool, ABC):
    def __init__(self, *, approval_mode: Literal["always_require", "never_require"] | None = None, folder_path: str = "."):
        super().__init__(name="markdown_read", description="Read a markdown file", approval_mode=approval_mode)
        self.folder_path = folder_path

    @override
    async def read_doc(self, doc_name: str)->str:
        with open(os.path.join(self.folder_path, doc_name + ".md"), "r") as f:
            return f.read()

class MarkdownToolFactory(DocToolFactory):
    def __init__(self, *, folder_path: str):
        self.folder_path = folder_path

    @override
    def create_doc_read_tool(self) -> DocReadTool:
        return MarkdownReadTool(folder_path=self.folder_path)

    @override
    def create_doc_write_tool(self) -> DocWriteTool:
        return MarkdownWriteTool(folder_path=self.folder_path)