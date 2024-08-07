import asyncio
from collections.abc import AsyncIterator

import sqlalchemy
from fastapi import Depends
from sqlalchemy import orm
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.session import Session

from waffledotcom.src.database.config import db_config
from waffledotcom.src.settings import settings
from waffledotcom.src.utils.singleton import SingletonMeta


class DBSessionFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._engine: sqlalchemy.Engine = sqlalchemy.create_engine(
            db_config.url,
            echo=settings.is_local,
            pool_recycle=28000,
            pool_pre_ping=True,
        )
        self._session_maker = orm.sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    def get_engine(self) -> sqlalchemy.Engine:
        return self._engine

    async def make_session(self) -> orm.Session:
        exc = RuntimeError("이게 실행되면 버그이다.")
        for _ in range(5):
            try:
                session = self._session_maker()
                return session
            except DatabaseError as e:
                exc = e
                await asyncio.sleep(1)
        raise exc

    def teardown(self):
        orm.close_all_sessions()
        self._engine.dispose()


async def get_db_session() -> AsyncIterator[orm.Session]:
    session = await DBSessionFactory().make_session()

    try:
        yield session
    finally:
        session.commit()
        session.close()


class Transaction:
    """
    A context manager class for flushing changes to the database without committing
    the transaction. This class can be used to check for integrity errors before
    committing the transaction. The transaction is committed when the scope of each
    request is finished. See `get_db_session` for more details.
    """

    def __init__(self, session: Session = Depends(get_db_session)):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            # rollback and let the exception propagate
            self._session.rollback()
            return False

        self._session.flush()
        return True
