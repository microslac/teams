from core.services import BaseService

from teams.models import Team


class TeamService(BaseService):
    @classmethod
    def create_team(cls, creator_id: str, *, data: dict) -> Team:
        name = data.pop("name")
        domain = data.pop("domain")
        team = Team.objects.create(creator_id=creator_id, name=name, domain=domain)
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
