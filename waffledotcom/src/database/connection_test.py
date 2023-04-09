from sqlalchemy import orm

from src.database.models import user as user_model


def test_db_connection(api_mock_client):
    session: orm.Session = api_mock_client.app.session_factory()
    assert isinstance(session, orm.Session)

    # Temporary Example
    session.add(user_model.User(name="fivessun"))

    users = session.query(user_model.User.name).all()
    assert len(users) == 1
    assert users[0][0] == "fivessun"
