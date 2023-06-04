import os

import sqlalchemy
from sqlalchemy import engine
from sqlalchemy import orm

from src.database import config
from src.utils import singleton_utils


class SQLAlchemyHandler(metaclass=singleton_utils.SingletonMeta):
    _engine: sqlalchemy.Engine | None
    _session_factory: orm.sessionmaker | None

    def __init__(self):
        # pylint:disable=pointless-string-statement
        if os.environ.get("TEST", "") == "True":
            self._engine = None
            self._session_factory = None
        else:
            db_config = config.DBConfig()
            self._engine: sqlalchemy.Engine = sqlalchemy.create_engine(
                engine.URL(
                    "mysql",
                    username=db_config.username,
                    password=db_config.password,
                    host=db_config.host,
                    port=db_config.port,
                    database=db_config.database,
                    query={},
                )
            )
            self.__session_factory = orm.sessionmaker(bind=self._engine)
            """

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
        session = self.session_factory()  # pylint:disable=not-callable
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
