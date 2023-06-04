from sqlite3 import IntegrityError

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from waffledotcom.src.database.connection import get_db_session
from waffledotcom.src.database.models.dummy import DummyModel


class DummyRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def get_dummy(self, name: str) -> DummyModel | None:
        query = select(DummyModel).where(DummyModel.name == name)
        return self.session.execute(query).scalar_one_or_none()

    def create_dummy(self, name: str) -> DummyModel:
        dummy = DummyModel(name=name)
        self.session.add(dummy)

        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise e

        return dummy
