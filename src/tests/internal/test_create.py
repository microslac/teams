from random import randint

import pytest
from rest_framework import status

from tests.internal import InternalTestBase


class TestTeamsCrud(InternalTestBase):
    def test_create_team_invalid_credentials(self):
        resp = self.client_request(f"{self.URL}/create", base=True, status=status.HTTP_403_FORBIDDEN)
        assert resp.ok is False

    @pytest.mark.parametrize("payload", [("", ""), ("", "team.com"), ("team", ""), ("team", "team@example")])
    def test_create_team_invalid_data(self, payload):
        name, domain = payload
        data = dict(name=name, domain=domain)
        resp = self.client_request(f"{self.URL}/create", data=data, internal=True, status=400, ok=False)
        if not name or not domain:
            assert resp.error == "blank"
        else:
            assert resp.error == "invalid"

    def team_create_team_duplicated(self):
        pass

    @pytest.mark.parametrize("payload", [("team", "team.com")])
    def test_create_team_success(self, payload):
        name, domain = payload
        auth_id = "A0123456789"
        is_open = bool(randint(0, 1))
        data = dict(creator=auth_id, name=name, domain=domain, is_open=is_open)
        resp = self.client_request(f"{self.URL}/create", data=data, internal=True, status=200, ok=True)
        assert resp.team.id.startswith("T")
        assert resp.team.name == name
        assert resp.team.domain == domain
        assert resp.team.creator == auth_id
        assert resp.team.is_open == is_open
