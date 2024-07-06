from sqlalchemy.orm import Session

from waffledotcom.src.apps.team.models import Team
from waffledotcom.src.apps.user.models import User


def test_create_team(db_session: Session, team: Team):
    db_session.add(team)
    db_session.commit()

    teams = db_session.query(Team).all()
    assert len(teams) == 1
    assert teams[0].name == team.name
    assert teams[0].introduction == team.introduction


def test_on_delete_team(db_session: Session, user: User, team: Team):
    team.users.append(user)

    db_session.add(user)
    db_session.add(team)
    db_session.commit()

    db_session.delete(team)
    db_session.commit()

    users = db_session.query(User).all()
    teams = db_session.query(Team).all()

    assert len(teams) == 0
    assert len(users) == 1


def test_on_delete_user_with_team(db_session: Session, user: User, team: Team):
    team.users.append(user)

    db_session.add(user)
    db_session.add(team)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    users = db_session.query(User).all()
    teams = db_session.query(Team).all()

    assert len(users) == 0
    assert len(teams) == 1
    assert len(teams[0].users) == 0


def test_assign_user_to_team(db_session: Session, user: User, team: Team):
    team.users.append(user)

    db_session.add(user)
    db_session.add(team)
    db_session.commit()

    users = db_session.query(User).all()
    teams = db_session.query(Team).all()

    assert len(users) == 1
    assert len(teams) == 1
    assert teams[0].users[0].username == user.username
