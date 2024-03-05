from tests.factories import TeamFactory
from tests.internal import InternalTestBase


class TestReadTeams(InternalTestBase):
    def test_lookup_team_success(self):
        team = TeamFactory()
        data = dict(id=team.id)
        resp = self.client_request(f"{self.URL}/lookup", internal=True, data=data, status=200, ok=True)

        assert resp.team.id == team.id
