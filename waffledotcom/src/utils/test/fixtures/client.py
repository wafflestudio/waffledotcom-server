from fastapi import testclient
import pytest

from src import app as app_factory


@pytest.fixture(scope="session")
def api_mock_client(db_engine, session_factory):
    app = app_factory.create_app()
    app.engine = db_engine
    app.session_factory = session_factory
    client = testclient.TestClient(app)

    yield client
    client.close()
