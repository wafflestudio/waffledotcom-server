from typing import Iterable

import pytest
import sqlalchemy
from sqlalchemy import orm

from waffledotcom.src.database.base import DeclarativeBase
from waffledotcom.src.database.config import DBConfig
from waffledotcom.src.settings import settings


@pytest.fixture(autouse=True, scope="session")
def set_test_env():
    settings.env = "test"


@pytest.fixture(scope="session")
def db_config() -> DBConfig:
    return DBConfig(_env_file=settings.env_files)  # type: ignore


@pytest.fixture(scope="session")
def db_engine(db_config: DBConfig) -> Iterable[sqlalchemy.Engine]:
    url = db_config.url
    engine = sqlalchemy.create_engine(url, echo=True)
    DeclarativeBase.metadata.create_all(bind=engine)

    try:
        yield engine
    finally:
        DeclarativeBase.metadata.drop_all(bind=engine)
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
