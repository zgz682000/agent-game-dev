from abc import ABC, abstractmethod
from agent_framework import Executor
from tool import Tool
from core.team_share_state import TeamShareState
class Role(ABC):
    def __init__(self, *, 
    name: str, 
    team_share_state: TeamShareState,
    leader: 'Role | None' = None, 
    downstream_roles: list['Role'] = [], 
    description: str | None = None, 
    instructions: str | None = None,
    tools: list[Tool] = []):
        self.name = name
        self.team_share_state = team_share_state
        self.leader = leader
        self.downstream_roles = downstream_roles
        self.description = description
        self.instructions = instructions
        self.tools = tools
    def __str__(self):
        return f"{self.name}: {self.description}"


    @abstractmethod
    def get_executor(self) -> Executor:
        raise NotImplementedError("Subclasses must implement this method")