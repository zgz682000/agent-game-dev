


from agent_framework import WorkflowContext, Executor, handler
from core.role import Role
from core.team_share_state import TeamShareState
from core.tool import Tool
from core.tools.doc_tool import DocReadTool, DocWriteTool


class GameDesignerExecutor(Executor):
    def __init__(self, * , designer: 'GameDesigner'):
        self.designer = designer
        self.client = designer.team_share_state.model_factory.create_reasoning_chat_client()
        self.agent = self.client.create_agent(
            name=self.designer.name, 
            description=self.designer.description, 
            instructions=self.designer.instructions, 
            tools=[
                tool.get_tool() for tool in self.designer.tools 
            ]
        )

    @handler
    async def handle(self, input: str, context: WorkflowContext[str]):
        pass

class GameDesigner(Role):
    def __init__(self, * , 
    name: str,
    team_share_state: TeamShareState,
    leader: 'Role | None' = None, 
    downstream_roles: list['Role'] = [],
    description: str | None = None,
    instructions: str | None = None,
    tools: list[Tool] = []):
        super().__init__(
            name=name or "Game Designer",
            team_share_state=team_share_state,
            description=description or "You are a game designer. You are responsible for designing the game.",
            instructions=instructions or "You are a game designer. You are responsible for designing the game.",
            leader=leader,
            downstream_roles=downstream_roles,
            tools=tools,
        )
        if any(tool for tool in tools if isinstance(tool, DocWriteTool)):
            self.tools.append(team_share_state.doc_tool_factory.create_doc_write_tool())
        if any(tool for tool in tools if isinstance(tool, DocReadTool)):
            self.tools.append(team_share_state.doc_tool_factory.create_doc_read_tool())

    def get_executor(self) -> Executor:
        return GameDesignerExecutor(designer=self)