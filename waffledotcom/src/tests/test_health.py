import http

from fastapi import testclient


def test_health(api_mock_client: testclient.TestClient):
    response = api_mock_client.get("/health")
    assert response.status_code == http.HTTPStatus.OK
