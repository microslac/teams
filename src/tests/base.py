import json
from types import SimpleNamespace

import pytest
from faker import Factory
from rest_framework.test import APIClient


@pytest.mark.django_db(databases=["default", "replication"])
class ApiTestBase:
    fake = Factory.create()
    client: APIClient

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def client_request(
        self,
        url: str,
        *,
        method: str = None,
        data: dict = None,
        format: str = None,
        ok: bool = None,
        status: int = None,
        client: APIClient = None
    ):
        data = data or {}
        format = format or "json"
        method = method or "post"
        assert method in ("get", "post", "put", "patch", "delete")

        client = client or self.client
        client_method = getattr(client, method)
        response = client_method(url, data=data, format=format)

        if status is not None:
            assert response.status_code == status
        resp = self.objectify(response.data)
        if ok is not None:
            assert resp.ok == ok
        return resp

    @staticmethod
    def objectify(data: dict):
        return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))


@pytest.mark.django_db(databases=["default", "replication"])
class UnitTestBase:
    def objectify(self, data: dict):
        return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
