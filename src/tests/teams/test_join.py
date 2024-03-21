from teams.models import Team
from tests.factories import TeamFactory
from tests.teams import TeamsTestBase


class TestJoinTeam(TeamsTestBase):
    def test_destroy_team_success(self, internal_client):
        team = TeamFactory()
        data = dict(id=team.id)
        self.client_request(f"{self.URL}/destroy", data=data, client=internal_client, status=200, ok=True)

        teams = Team.objects.include_deleted()
        assert len(teams) == 0
