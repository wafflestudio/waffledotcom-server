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
        db_engine = sqlalchemy.create_engine(url)

        DeclarativeBase.metadata.create_all(bind=db_engine)

        try:
            yield db_engine
        finally:
            db_engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine: sqlalchemy.Engine) -> Iterable[orm.Session]:
    connection = db_engine.connect()
    transaction = connection.begin_nested()

    session_maker = orm.sessionmaker(
        connection,
        expire_on_commit=False,
    )

    session = session_maker()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
