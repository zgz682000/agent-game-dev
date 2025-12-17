
from typing import Any
from core.tools.doc_tool import DocToolFactory   
from core.model_factory import ModelFactory
class TeamShareState():
    def __init__(
        self, *, 
        model_factory: ModelFactory,
        doc_tool_factory: DocToolFactory,
        extra_properties: dict[str, Any] = {}
    ):
        self.model_factory = model_factory
        self.extra_properties = extra_properties
        self.doc_tool_factory = doc_tool_factory

    