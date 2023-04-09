import tempfile

import pytest
import sqlalchemy
from sqlalchemy import orm

from src.database.models import base


@pytest.fixture(scope="session", name="db_engine")
def fixture_engine() -> sqlalchemy.Engine:
    with tempfile.TemporaryDirectory() as tmpdirname:
        url = f"sqlite:////Waffle/Waffledotcom/waffledotcom-server/waffledotcom/test"
        db_engine = sqlalchemy.create_engine(url)

        yield db_engine
        db_engine.dispose()


@pytest.fixture(scope="session")
def db_session(db_engine: sqlalchemy.Engine) -> orm.Session:
    connection = db_engine.connect()
    trans = connection.begin()

    session_maker = orm.sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    # create database
    base.BaseModel.metadata.create_all(bind=db_engine)

    yield session

    session.close()
    trans.rollback()
    connection.close()
