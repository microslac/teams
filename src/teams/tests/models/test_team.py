from teams.models import Team
from tests.base import UnitTestBase


class TestTeamModel(UnitTestBase):
    def test_create_team(self):
        team = Team(name="team", domain="team.com")

        assert team.uuid
        assert team.name == "team"
        assert team.id.startswith("T")
        assert team.domain == "team.com"
