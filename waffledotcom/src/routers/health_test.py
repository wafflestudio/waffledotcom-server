import http

from fastapi import testclient
import pytest


@pytest.mark.asyncio
async def test_read_profile(api_mock_client: testclient.TestClient):
    response = api_mock_client.get("/health")
    assert response.status_code == http.HTTPStatus.OK
