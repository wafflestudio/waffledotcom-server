import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from waffledotcom.src.database.models.position import Position
from waffledotcom.src.database.models.user import User


def test_create_position(db_session: Session, position: Position):
    db_session.add(position)
    db_session.commit()

    positions = db_session.query(Position).all()
    assert len(positions) == 1
    assert positions[0].name == position.name


def test_add_position_with_same_name(db_session: Session, position: Position):
    db_session.add(position)
    db_session.flush()

    positions = db_session.query(Position).all()
    assert len(positions) == 1
    assert positions[0].name == position.name

    position = Position(
        name=position.name,
    )

    db_session.add(position)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_on_delete_position(db_session: Session, user: User, position: Position):
    position.users.append(user)

    db_session.add(user)
    db_session.add(position)
    db_session.commit()

    db_session.delete(position)
    db_session.commit()

    users = db_session.query(User).all()
    positions = db_session.query(Position).all()

    assert len(users) == 1
    assert len(positions) == 0


def test_assign_user_to_position(db_session: Session, user: User, position: Position):
    position.users.append(user)

    db_session.add(user)
    db_session.add(position)
    db_session.commit()

    users = db_session.query(User).all()
    positions = db_session.query(Position).all()

    assert len(users) == 1
    assert len(positions) == 1
    assert positions[0].users[0].username == user.username


def test_on_delete_user_with_position(
    db_session: Session, user: User, position: Position
):
    user.positions.append(position)

    db_session.add(user)
    db_session.add(position)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    users = db_session.query(User).all()
    positions = db_session.query(Position).all()

    assert len(users) == 0
    assert len(positions) == 1
