from core.team_share_state import TeamShareState
from role import Role
from agent_framework import Workflow

class Team():
    def __init__(self, *, name: str, team_share_state: TeamShareState, roles: list[Role], leader_role: Role | None = None, sub_teams: list['Team'] = []):
        self._name = name
        self._team_share_state = team_share_state
        self._roles = roles
        self._leader_role = leader_role
        self._sub_teams = sub_teams
        for role in roles:
            role.team_share_state = team_share_state
            role.leader = leader_role

    @property
    def name(self) -> str:
        return self._name

    @property
    def leader_role(self) -> Role | None:
        return self._leader_role

    def __str__(self):
        return f"{self.name}"

    def build_workflow(self) -> Workflow:
        raise NotImplementedError("Must implement this method")