from tests.factories import TeamFactory
from tests.teams import TeamsTestBase


class TestReadTeams(TeamsTestBase):
    def test_lookup_team_success(self, internal_client):
        team = TeamFactory()
        data = dict(id=team.id)
        resp = self.client_request(f"{self.URL}/lookup", client=internal_client, data=data, status=200, ok=True)

        assert resp.team.id == team.id

    def test_info_team_success(self):
        pass
