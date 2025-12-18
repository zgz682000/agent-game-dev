
from asyncio import Future
from core.tool import Tool
from typing import Callable, Any
from agent_framework import ToolProtocol, AIFunction
from typing import override
from pydantic import BaseModel, Field
from agent_framework import WorkflowContext
from agent_framework import AgentExecutorResponse, AgentRunResponse


class SubmitOutputToUserInput(BaseModel):
    output: str = Field(description="The output to submit to the User") 

class SubmitOutputToUserResponse(BaseModel):
    response: str

class SubmitOutputToUserTool(Tool):
    def __init__(self):
        super().__init__(name="submit_output_to_user", approval_mode="never_require")
        self._description = "Submit your output to the User, and wait for User's response"
        self.__workflow_context: WorkflowContext[AgentExecutorResponse, AgentRunResponse] | None = None
        self.__future: Future[str] | None = None
    
    def set_workflow_context(self, workflow_context: WorkflowContext[AgentExecutorResponse, AgentRunResponse]) -> None:
        self.__workflow_context = workflow_context
    
    async def _submit_output_to_user(self, output: str) -> str:
        if not self.__workflow_context:
            raise ValueError("Workflow context is not set")
        self.__future = Future()
        await self.__workflow_context.request_info(SubmitOutputToUserInput(output=output), response_type=SubmitOutputToUserResponse)
        return await self.__future

    async def handle_submit_output_to_user_response(self, original_request: SubmitOutputToUserInput, response: SubmitOutputToUserResponse, ctx: WorkflowContext[AgentExecutorResponse, AgentRunResponse]) -> None:
        if self.__future is None:
            raise ValueError("Future is not set")
        self.__future.set_result(response.response)

    @override
    def get_tool(self) -> ToolProtocol | Callable[..., Any]:
        return AIFunction(
            name=self._name,
            func=self._submit_output_to_user,
            input_model=SubmitOutputToUserInput,
            description=self._description,
            approval_mode=self._approval_mode,
        )