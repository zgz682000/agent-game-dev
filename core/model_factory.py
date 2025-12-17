from abc import ABC, abstractmethod
from typing import Any, Optional, override
from agent_framework import BaseChatClient
from agent_framework.openai import OpenAIChatClient

class ModelFactory(ABC):

    @abstractmethod
    def create_chat_client(self, **kwargs: Any) -> BaseChatClient:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def create_reasoning_chat_client(self, **kwargs: Any) -> BaseChatClient:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def create_flash_chat_client(self, **kwargs: Any) -> BaseChatClient:
        raise NotImplementedError("Subclasses must implement this method")

class OpenAIModelFactory(ModelFactory):

    def __init__(self, *,
    api_key: str,
    base_url: str,
    model_id: str,
    reasoning_model_id: Optional[str] = None,
    flash_model_id: Optional[str] = None,
    **kwargs: Any):
        self.api_key = api_key
        self.base_url = base_url
        self.model_id = model_id
        self.reasoning_model_id = reasoning_model_id
        self.flash_model_id = flash_model_id or model_id
    @override
    def create_chat_client(self, **kwargs: Any) -> BaseChatClient:
        return OpenAIChatClient(
            api_key=self.api_key,
            base_url=self.base_url,
            model_id=self.model_id,
            **kwargs
        )
    
    @override
    def create_reasoning_chat_client(self, **kwargs: Any) -> BaseChatClient:
        return OpenAIChatClient(
            api_key=self.api_key,
            base_url=self.base_url,
            model_id=self.reasoning_model_id,
            **kwargs
        )
    
    @override
    def create_flash_chat_client(self, **kwargs: Any) -> BaseChatClient:
        return OpenAIChatClient(
            api_key=self.api_key,
            base_url=self.base_url,
            model_id=self.flash_model_id,
            **kwargs
        )