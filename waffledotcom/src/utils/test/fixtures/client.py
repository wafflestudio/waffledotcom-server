from fastapi import testclient
import pytest

from src import app as app_factory


@pytest.fixture(scope="session")
def api_mock_client(db_session):
    app = app_factory.create_app()
    app.session = db_session
    client = testclient.TestClient(app)

    yield client
    client.close()
