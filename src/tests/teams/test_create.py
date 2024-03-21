import pytest
from random import randint
from rest_framework import status

from tests.teams import TeamsTestBase


class TestTeamsCrud(TeamsTestBase):
    def test_create_team_invalid_credentials(self, base_client):
        resp = self.client_request(f"{self.URL}/create", client=base_client, status=status.HTTP_403_FORBIDDEN)
        assert resp.ok is False

    @pytest.mark.parametrize("payload", [("", ""), ("", "team.com"), ("team", ""), ("team", "team@example")])
    def test_create_team_invalid_data(self, client, payload):
        name, domain = payload
        data = dict(name=name, domain=domain)
        resp = self.client_request(f"{self.URL}/create", data=data, status=status.HTTP_400_BAD_REQUEST, ok=False)
        if not name or not domain:
            assert resp.error == "blank"
        else:
            assert resp.error == "invalid"

    def team_create_team_duplicated(self):
        pass

    @pytest.mark.parametrize("payload", [("team", "team.com")])
    def test_create_team_success(self, client, payload):
        name, domain = payload
        is_open = bool(randint(0, 1))
        data = dict(name=name, domain=domain, is_open=is_open)
        resp = self.client_request(f"{self.URL}/create", data=data, status=status.HTTP_200_OK, ok=True)
        assert resp.team.id.startswith("T")
        assert resp.team.name == name
        assert resp.team.domain == domain
        assert resp.team.creator is not None
        assert resp.team.is_open == is_open
