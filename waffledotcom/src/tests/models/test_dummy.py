import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from waffledotcom.src.apis.dummy.repository import DummyRepository


def test_create_dummy(db_session: Session):
    repository = DummyRepository(db_session)
    dummy = repository.create_dummy(name="test")
    assert dummy.id == 1 and dummy.name == "test"


def test_create_dummy_duplicate(db_session: Session):
    repository = DummyRepository(db_session)
    repository.create_dummy(name="test")
    with pytest.raises(IntegrityError):
        repository.create_dummy(name="test")
