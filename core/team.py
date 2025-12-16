from role import Role
from agent_framework import Workflow

class Team():
    def __init__(self, *, name: str, roles: list[Role], leader_role: Role | None = None, sub_teams: list['Team'] = []):
        self.name = name
        self.roles = roles
        self.leader_role = leader_role
        self.sub_teams = sub_teams

    def __str__(self):
        return f"{self.name}"

    def build_workflow(self) -> Workflow:
        raise NotImplementedError("Must implement this method")