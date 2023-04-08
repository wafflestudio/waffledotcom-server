from fastapi import testclient
import pytest

from src import app as app_factory


@pytest.fixture(scope="session")
def api_mock_client():
    app = app_factory.create_app()
    client = testclient.TestClient(app)
    return client
