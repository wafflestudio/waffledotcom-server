import tempfile

import pytest
import sqlalchemy
from sqlalchemy import orm

from src.database.models import base


@pytest.fixture(scope="session", name="db_engine")
def fixture_engine() -> sqlalchemy.Engine:
    with tempfile.TemporaryDirectory() as tmpdirname:
        url = f"sqlite:////{tmpdirname}/db.sqlite3"
        db_engine = sqlalchemy.create_engine(url)

        try:
            yield db_engine
        finally:
            db_engine.dispose()


@pytest.fixture(scope="session", name="session_factory")
def fixture_session_factory(db_engine: sqlalchemy.Engine) -> orm.Session:
    connection = db_engine.connect()
    trans = connection.begin()

    session_factory = orm.sessionmaker(
        connection,
        expire_on_commit=False,
    )

    # create database
    base.DeclarativeBase.metadata.create_all(bind=db_engine)

    try:
        yield session_factory
    finally:
        trans.rollback()
        connection.close()
