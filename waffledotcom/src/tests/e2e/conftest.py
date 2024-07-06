import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from waffledotcom.src.apps.router import api_router
from waffledotcom.src.database.connection import get_db_session


@pytest.fixture
def test_client(db_session: Session) -> TestClient:
    app = FastAPI()
    app.include_router(api_router)

    def override_get_db_session():
        return db_session

    app.dependency_overrides[get_db_session] = override_get_db_session
    client = TestClient(app)
    return client
