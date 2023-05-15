import os

import sqlalchemy
from sqlalchemy import engine
from sqlalchemy import orm

from waffledotcom.src.database.config import DBConfig
from waffledotcom.src.utils.singleton import SingletonMeta


class SQLAlchemyHandler(metaclass=singleton.SingletonMeta):
    _engine: sqlalchemy.Engine | None
    _session_factory: orm.sessionmaker | None

    def __init__(self):
        self.engine: sqlalchemy.Engine = sqlalchemy.create_engine(DBConfig().url)
        self.session_maker = orm.sessionmaker(bind=self.engine, expire_on_commit=False)

    @property
    def engine(self) -> sqlalchemy.Engine:
        if not self._engine:
            raise RuntimeError("Engine is not created.")
        return self._engine

    @property
    def session_factory(self) -> orm.sessionmaker:
        if not self._session_factory:
            raise RuntimeError("Session factory is not created.")
        return self._session_factory

    def get_session(self) -> orm.Session:
        session = self.session_factory()
        try:
            yield session
        finally:
            session.commit()
            session.close()

    def __del__(self):
        if self._session_factory:
            self._session_factory.close_all()
        if self._engine:
            self._engine.dispose()


def get_db_connection():
    return SQLAlchemyHandler()
