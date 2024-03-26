from micro.jango.services import BaseService

from teams.models import Team
from teams.sagas.join_team import JoinTeamSaga


class TeamService(BaseService):
    @classmethod
    def get_team(cls, team_id: str) -> Team:
        return Team.objects.get(id=team_id)

    @classmethod
    def create_team(cls, creator_id: str, *, data: dict) -> Team:
        name = data.pop("name")
        domain = data.pop("domain")
        is_open = data.pop("is_open", False)
        team = Team.objects.create(creator_id=creator_id, name=name, domain=domain, is_open=is_open)
        return team

    @classmethod
    def save_team(cls, instance: Team = None, **data) -> Team:
        try:
            created = False
            if instance:
                team = instance
            else:
                team = Team()
                created = True

            for key, value in data.items():
                setattr(team, key, value)
            team.save()
            if created:
                pass
            return team
        except Exception as ex:
            raise ex

    @classmethod
    def lookup_team(cls, team_id: str) -> dict | None:
        return Team.objects.filter(id=team_id).values("id").first()

    @classmethod
    def destroy_team(cls, team_id: str):
        team = Team.objects.get(id=team_id)
        team.destroy()

    @classmethod
    def join_team(cls, team_id: str, auth_id: str) -> Team:
        team = cls.get_team(team_id)
        saga = JoinTeamSaga(team_id=team.id, auth_id=auth_id)
        saga.run()
        return team
