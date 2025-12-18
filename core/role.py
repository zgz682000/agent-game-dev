from abc import ABC, abstractmethod
from agent_framework import Executor
from core.tools.submit_output_to_user_tool import SubmitOutputToUserInput, SubmitOutputToUserResponse, SubmitOutputToUserTool
from tool import Tool
from core.team_share_state import TeamShareState
from core.prompts.role_prompts import SUBMIT_OUTPUT_TO_LEADER_PROMPT
from typing import override
from agent_framework import AgentExecutor, WorkflowContext
from agent_framework import AgentExecutorResponse, AgentRunResponse, response_handler, ChatAgent


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
        self._name = name
        self._team_share_state = team_share_state
        self._leader = leader
        self._downstream_role = downstream_role
        self._skill_description = skill_description
        self._duty_description = duty_description
        self._other_descriptions = other_descriptions
        self._submit_output_instruction = submit_output_instruction
        if not self._submit_output_instruction:
            self._submit_output_instruction = SUBMIT_OUTPUT_TO_LEADER_PROMPT.format(leader=leader.name if leader else "User", downstream_role=downstream_role.name if downstream_role else "User")
        self._other_instructions = other_instructions
        self._tools = tools
        self._workflow_context: WorkflowContext[AgentExecutorResponse, AgentRunResponse] | None = None

    def __str__(self):
        return f"{self._name}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f'''
# Role Description
* Your name: 
    {self._name}
* Your skill: 
    {self._skill_description}
* Your duty: 
    {self._duty_description}
* Other descriptions: 
    {self._other_descriptions or ""}
'''

    @property
    def instructions(self) -> str:
        return f'''
# Role Instructions
* Submit output instruction: 
    {self._submit_output_instruction}
* Other instructions: 
    {self._other_instructions or ""}
'''

    @property
    def team_share_state(self) -> TeamShareState:
        return self._team_share_state

    @team_share_state.setter
    def team_share_state(self, team_share_state: TeamShareState) -> None:
        self._team_share_state = team_share_state

    @property
    def leader(self) -> 'Role | None':
        return self._leader
    
    @leader.setter
    def leader(self, leader: 'Role | None') -> None:
        self._leader = leader

    @abstractmethod
    def get_executor(self) -> Executor:
        raise NotImplementedError("Subclasses must implement this method")



    class RoleExecutor(AgentExecutor):
        def __init__(self, * , role: 'Role', agent: ChatAgent | None = None):
            self._role = role
            client = role._team_share_state.model_factory.create_reasoning_chat_client()
            
            """
            If the role has no leader, it means the User is the leader. So we need create a submit output to user tool to submit the output to the User.
            """
            if self._role._leader is None:
                self.__submit_output_to_user_tool = next((tool for tool in self._role._tools if isinstance(tool, SubmitOutputToUserTool)), None)
                if not self.__submit_output_to_user_tool:
                    self.__submit_output_to_user_tool = SubmitOutputToUserTool()
                    self._role._tools.append(self.__submit_output_to_user_tool)
            if agent is None:
                agent = client.create_agent(
                    name=self._role._name, 
                    description=self._role.description, 
                    instructions=self._role.instructions, 
                    tools=[
                        tool.get_tool() for tool in self._role._tools 
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