import tempfile
from typing import Iterable

import pytest
import sqlalchemy
from sqlalchemy import orm

from waffledotcom.src.database.models.base import DeclarativeBase


@pytest.fixture(scope="session")
def db_engine() -> Iterable[sqlalchemy.Engine]:
    with tempfile.TemporaryDirectory() as tmpdirname:
        url = f"sqlite:////{tmpdirname}/db.sqlite3"
        engine = sqlalchemy.create_engine(url)
        DeclarativeBase.metadata.create_all(bind=engine)

        try:
            yield engine
        finally:
            engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine: sqlalchemy.Engine) -> Iterable[orm.Session]:
    connection = db_engine.connect()
    transaction = connection.begin_nested()

    session_maker = orm.sessionmaker(
        connection,
        expire_on_commit=True,
    )

    session = session_maker()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
