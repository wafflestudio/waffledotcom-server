from sqlalchemy import orm

from src.database.models import user as user_model


def test_db_connection(api_mock_client):
    session: orm.Session = api_mock_client.app.session_factory()
    assert isinstance(session, orm.Session)

    # Temporary Example
    session.add(user_model.User(
        username='test',
        password='test',
        first_name='test',
        last_name='test',
        student_id='test',
        department='test',
        college='test',
        phone_number='+821012345678',
        github_id='test',
        github_email='test@test.test',
        slack_id='test',
        slack_email='test@test.test',
        notion_email='test@test.test',
        generation=1,
        active=True,
        introduction='test'
    ))

    users = session.query(user_model.User.username).all()
    assert len(users) == 1
    assert users[0][0] == "test"
