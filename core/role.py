from abc import ABC, abstractmethod
from agent_framework import Executor
from core.tools.submit_output_to_user_tool import SubmitOutputToUserInput, SubmitOutputToUserResponse, SubmitOutputToUserTool
from tool import Tool
from core.team_share_state import TeamShareState
from core.prompts.role_prompts import SUBMIT_OUTPUT_TO_LEADER_PROMPT
from typing import override
from agent_framework import AgentExecutor, WorkflowContext
from agent_framework import AgentExecutorResponse, AgentRunResponse, response_handler
class RoleExecutor(AgentExecutor):
    def __init__(self, * , role: 'Role'):
        self.role = role
        self.client = role.team_share_state.model_factory.create_reasoning_chat_client()
        
        """
        If the role has no leader, it means the User is the leader. So we need create a submit output to user tool to submit the output to the User.
        """
        if self.role.leader is None:
            self.__submit_output_to_user_tool = next((tool for tool in self.role.tools if isinstance(tool, SubmitOutputToUserTool)), None)
            if not self.__submit_output_to_user_tool:
                self.__submit_output_to_user_tool = SubmitOutputToUserTool()
                self.role.tools.append(self.__submit_output_to_user_tool)
        agent = self.client.create_agent(
            name=self.role.name, 
            description=self.role.description, 
            instructions=self.role.instructions, 
            tools=[
                tool.get_tool() for tool in self.role.tools 
            ]
        )
        super().__init__(agent=agent)

    @override
    async def _run_agent_and_emit(self, ctx: WorkflowContext[AgentExecutorResponse, AgentRunResponse]) -> None:
        if self.__submit_output_to_user_tool:
            self.__submit_output_to_user_tool.set_workflow_context(ctx)
        return await super()._run_agent_and_emit(ctx)
    
    @response_handler
    async def handle_submit_output_to_user_response(
        self,
        original_request: SubmitOutputToUserInput,
        response: SubmitOutputToUserResponse,
        ctx: WorkflowContext[AgentExecutorResponse, AgentRunResponse],
    ) -> None:
        if self.__submit_output_to_user_tool:
            await self.__submit_output_to_user_tool.handle_submit_output_to_user_response(original_request, response, ctx)

class Role(ABC):
    def __init__(self, *, 
    name: str, 
    team_share_state: TeamShareState,
    leader: 'Role | None' = None, 
    downstream_role: 'Role | None' = None, 
    skill_description: str, 
    duty_description: str,
    other_descriptions: str | None = None,
    submit_output_instruction: str | None = None,
    other_instructions: str | None = None,
    tools: list[Tool] = []):
        self.name = name
        self.team_share_state = team_share_state
        self.leader = leader
        self.downstream_role = downstream_role
        self.skill_description = skill_description
        self.duty_description = duty_description
        self.other_descriptions = other_descriptions
        self.submit_output_instruction = submit_output_instruction
        if not self.submit_output_instruction:
            self.submit_output_instruction = SUBMIT_OUTPUT_TO_LEADER_PROMPT.format(leader=leader.name if leader else "User", downstream_role=downstream_role.name if downstream_role else "User")
        self.other_instructions = other_instructions
        self.tools = tools
        self.workflow_context: WorkflowContext[AgentExecutorResponse, AgentRunResponse] | None = None

    def __str__(self):
        return f"{self.name}"

    @property
    def description(self) -> str:
        return f'''
# Role Description
* Your name: 
    {self.name}
* Your skill: 
    {self.skill_description}
* Your duty: 
    {self.duty_description}
* Other descriptions: 
    {self.other_descriptions or ""}
'''

    @property
    def instructions(self) -> str:
        return f'''
# Role Instructions
* Submit output instruction: 
    {self.submit_output_instruction}
* Other instructions: 
    {self.other_instructions or ""}
'''

    @abstractmethod
    def get_executor(self) -> Executor:
        raise NotImplementedError("Subclasses must implement this method")