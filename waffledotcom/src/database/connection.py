from typing import Iterator

from fastapi import Depends
import sqlalchemy
from sqlalchemy import orm

from waffledotcom.src.database.config import DBConfig
from waffledotcom.src.utils.singleton import SingletonMeta


class DBSessionFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.engine: sqlalchemy.Engine = sqlalchemy.create_engine(DBConfig().url)
        self.session_maker = orm.sessionmaker(bind=self.engine, expire_on_commit=False)

    def make_session(self) -> orm.Session:
        session = self.session_maker()
        return session

    def teardown(self):
        orm.close_all_sessions()
        self.engine.dispose()


def get_db_session() -> Iterator[orm.Session]:
    session = DBSessionFactory().make_session()

    try:
        yield session
    finally:
        session.commit()
        session.close()
