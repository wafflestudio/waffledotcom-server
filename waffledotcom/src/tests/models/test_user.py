import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from waffledotcom.src.apps.user.models import User


def test_create_user(db_session: Session, user: User):
    db_session.add(user)
    db_session.flush()

    users = db_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "testuser"
    assert users[0].first_name == "Test"


def test_create_user_with_same_username(db_session: Session, user: User):
    db_session.add(user)
    db_session.flush()

    users = db_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "testuser"
    assert users[0].first_name == "Test"

    user = User(
        sso_id=user.sso_id,
        username=user.username,
        first_name="Test",
        last_name="User",
        is_active=True,
        is_admin=False,
    )

    db_session.add(user)

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_db_session_add_same_object_twice(db_session: Session, user: User):
    db_session.add(user)
    db_session.flush()

    user.username = "testuser2"
    db_session.add(user)
    db_session.flush()

    users = db_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "testuser2"
