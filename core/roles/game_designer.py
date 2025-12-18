


from agent_framework import AgentExecutor, Executor
from core.role import Role
from core.team_share_state import TeamShareState
from core.tool import Tool
from core.tools.doc_tool import DocReadTool, DocWriteTool
from core.prompts.game_designer_prompts import GAME_DESIGNER_SKILL_DESCRIPTION, GAME_DESIGNER_DUTY_DESCRIPTION, GAME_DESIGNER_OTHER_INSTRUCTIONS
class GameDesignerExecutor(AgentExecutor):
    def __init__(self, * , designer: 'GameDesigner'):
        self.designer = designer
        self.client = designer.team_share_state.model_factory.create_reasoning_chat_client()
        agent = self.client.create_agent(
            name=self.designer.name, 
            description=self.designer.description, 
            instructions=self.designer.instructions, 
            tools=[
                tool.get_tool() for tool in self.designer.tools 
            ]
        )
        super().__init__(agent=agent)


class GameDesigner(Role):
    def __init__(self, * , 
    name: str,
    team_share_state: TeamShareState,
    leader: 'Role | None' = None, 
    downstream_role: 'Role | None' = None,
    description: str | None = None,
    instructions: str | None = None,
    tools: list[Tool] = []):
        game_type = team_share_state.extra_properties.get("game_type", "Casual Game")
        platform = team_share_state.extra_properties.get("platform", "PC Web Browser")
        super().__init__(
            name=name or "Game Designer",
            team_share_state=team_share_state,
            skill_description=GAME_DESIGNER_SKILL_DESCRIPTION.format(game_type=game_type, platform=platform),
            duty_description=GAME_DESIGNER_DUTY_DESCRIPTION.format(doc_format_name=team_share_state.doc_tool_factory.doc_format_name),
            other_instructions=GAME_DESIGNER_OTHER_INSTRUCTIONS,
            leader=leader,
            downstream_role=downstream_role,
            tools=tools,
        )
        if not any(tool for tool in tools if isinstance(tool, DocWriteTool)):
            self.tools.append(team_share_state.doc_tool_factory.create_doc_write_tool())
        if not any(tool for tool in tools if isinstance(tool, DocReadTool)):
            self.tools.append(team_share_state.doc_tool_factory.create_doc_read_tool())

    def get_executor(self) -> Executor:
        return GameDesignerExecutor(designer=self)