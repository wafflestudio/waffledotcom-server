import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from waffledotcom.src.database.models.user import User


def test_create_user(db_session: Session, user: User):
    db_session.add(user)
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "testuser"
    assert users[0].first_name == "Test"


def test_create_user_with_same_username(db_session: Session, user: User):
    db_session.add(user)
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "testuser"
    assert users[0].first_name == "Test"

    user = User(
        username=user.username,
        password="testpassword",
        first_name="Test",
        last_name="User",
        is_active_member=True,
        is_admin=False,
    )

    db_session.add(user)

    with pytest.raises(IntegrityError):
        db_session.commit()
