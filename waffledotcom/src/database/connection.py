from typing import Iterator

from fastapi import Depends
import sqlalchemy
from sqlalchemy import orm

from waffledotcom.src.database.config import DBConfig
from waffledotcom.src.utils.singleton import SingletonMeta


class DBSessionFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._engine: sqlalchemy.Engine = sqlalchemy.create_engine(DBConfig().url)
        self._session_maker = orm.sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    def make_session(self) -> orm.Session:
        session = self._session_maker()
        return session

    def teardown(self):
        orm.close_all_sessions()
        self._engine.dispose()


def get_db_session() -> Iterator[orm.Session]:
    session = DBSessionFactory().make_session()

    try:
        yield session
    finally:
        session.commit()
        session.close()
