from teams.models import Team
from tests.factories import TeamFactory
from tests.internal import InternalTestBase


class TestDeleteTeam(InternalTestBase):
    def test_destroy_team_success(self):
        team = TeamFactory()
        data = dict(id=team.id)
        self.client_request(f"{self.URL}/destroy", data=data, internal=True, status=200, ok=True)

        teams = Team.objects.include_deleted()
        assert len(teams) == 0
