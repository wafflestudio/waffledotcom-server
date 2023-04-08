import os

import sqlalchemy
from sqlalchemy import engine
from sqlalchemy import orm

from src.database import config
from src.utils import singleton_utils


class SQLAlchemyHandler(metaclass=singleton_utils.SingletonMeta):
    def __init__(self):
        if os.environ.get("TEST", "") == "True":
            self._engine = None
            self._session = None
        else:
            """Need To Test
            db_config = config.DBConfig()
            self._engine: sqlalchemy.Engine = sqlalchemy.create_engine(
                engine.URL(
                    "mysql",
                    username=db_config.username,
                    password=db_config.password,
                    host=db_config.host,
                    port=db_config.port,
                )
            )
            _session_maker = orm.sessionmaker(bind=self._engine)
            self._session = _session_maker()
            """

    @property
    def session(self) -> orm.Session:
        return self._session

    @session.setter
    def session(self, param):
        self._session = param

    def __del__(self):
        if self._engine:
            self._engine.dispose()
        if self._session:
            self._session.close()


def get_db_connection():
    return SQLAlchemyHandler()
