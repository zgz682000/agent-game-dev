
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
        self._model_factory = model_factory
        self._extra_properties = extra_properties
        self._doc_tool_factory = doc_tool_factory

    @property
    def model_factory(self) -> ModelFactory:
        return self._model_factory

    @property
    def extra_properties(self) -> dict[str, Any]:
        return self._extra_properties

    @property
    def doc_tool_factory(self) -> DocToolFactory:
        return self._doc_tool_factory