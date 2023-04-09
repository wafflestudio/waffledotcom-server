from sqlalchemy import orm

from src.database.models import team, position, sns, user

test_user_kwargs = {
    'username':'test',
    'password':'test',
    'first_name':'test',
    'last_name':'test',
    'student_id':'test',
    'department':'test',
    'college':'test',
    'phone_number':'+821012345678',
    'github_id':'test',
    'github_email':'test@test.test',
    'slack_id':'test',
    'slack_email':'test@test.test',
    'notion_email':'test@test.test',
    'generation':1,
    'active':True,
    'introduction':'test'}
test_team_kwargs = {
    'name':'test',
    'introduction':'test'
}
test_position_kwargs = {
    'name':'test_position'
}
test_sns_kwargs = {
    'name':'testagram',
    'url':'@waffle'
}



def test_user_model(api_mock_client):
    session: orm.Session = api_mock_client.app.session
    assert isinstance(session, orm.Session)

    session.query(user.User).delete()
    session.commit()

    # Temporary Example
    session.add(user.User(**test_user_kwargs))

    users = session.query(user.User).all()
    assert len(users) == 1
    assert users[0].username == "test"
    assert users[0].password == "test"
    assert users[0].first_name == "test"
    assert users[0].last_name == "test"
    assert users[0].student_id == "test"
    assert users[0].department == "test"
    assert users[0].college == "test"
    assert users[0].phone_number.e164 == "+821012345678"
    assert users[0].github_id == "test"
    assert users[0].github_email == "test@test.test"
    assert users[0].slack_id == "test"
    assert users[0].slack_email == "test@test.test"
    assert users[0].notion_email == "test@test.test"
    assert users[0].generation == 1
    assert users[0].active == True
    assert users[0].introduction == "test"


def test_team_model(api_mock_client):
    session: orm.Session = api_mock_client.app.session
    assert isinstance(session, orm.Session)

    session.query(team.Team).delete()
    session.commit()

    # Temporary Example
    session.add(team.Team(**test_team_kwargs))

    teams = session.query(team.Team).all()
    assert len(teams) == 1
    assert teams[0].name == "test"
    assert teams[0].introduction == "test"


def test_position_model(api_mock_client):
    session: orm.Session = api_mock_client.app.session
    assert isinstance(session, orm.Session)

    session.query(position.Position).delete()
    session.query(user.User).delete()
    session.commit()

    # Temporary Example

    test_user_kwargs2 = test_user_kwargs.copy()
    test_user_kwargs2['username'] = 'test2'

    test_position_kwargs2 = test_position_kwargs.copy()
    test_position_kwargs2['name'] = 'test2'

    test_user = user.User(**test_user_kwargs)
    test_user2 = user.User(**test_user_kwargs2)

    test_positon = position.Position(**test_position_kwargs)
    test_position2 = position.Position(**test_position_kwargs2)

    test_user.positions.append(test_positon)
    test_user.positions.append(test_position2)
    test_user2.positions.append(test_position2)

    session.add(test_user)
    session.add(test_user2)
    session.commit()

    test_user_from_query = session.query(user.User).first()

    assert len(test_user_from_query.positions) == 2
    assert test_user_from_query.positions[0].p_idx == test_positon.p_idx
    assert len(test_user_from_query.positions[0].users) == 1
    assert test_user_from_query.positions[0].users[0].u_idx == test_user.u_idx

    assert test_user_from_query.positions[1].p_idx == test_position2.p_idx
    assert len(test_user_from_query.positions[1].users) == 2
    assert test_user_from_query.positions[1].users[0].u_idx == test_user.u_idx
    assert test_user_from_query.positions[1].users[1].u_idx == test_user2.u_idx


def test_team_user_association_model(api_mock_client):
    session: orm.Session = api_mock_client.app.session
    assert isinstance(session, orm.Session)

    session.query(team.Team).delete()
    session.query(user.User).delete()
    session.commit()

    # Temporary Example

    test_user_kwargs2 = test_user_kwargs.copy()
    test_user_kwargs2['username'] = 'test2'

    test_team_kwargs2 = test_team_kwargs.copy()
    test_team_kwargs2['name'] = 'test2'

    test_user = user.User(**test_user_kwargs)
    test_user2 = user.User(**test_user_kwargs2)

    test_team = team.Team(**test_team_kwargs)
    test_team2 = team.Team(**test_team_kwargs2)

    test_user.teams.append(test_team)
    test_user.teams.append(test_team2)
    test_user2.teams.append(test_team2)

    session.add(test_user)
    session.add(test_user2)
    session.commit()

    test_user_from_query = session.query(user.User).first()

    assert len(test_user_from_query.teams) == 2
    assert test_user_from_query.teams[0].t_idx == test_team.t_idx
    assert len(test_user_from_query.teams[0].users) == 1
    assert test_user_from_query.teams[0].users[0].u_idx == test_user.u_idx

    assert test_user_from_query.teams[1].t_idx == test_team2.t_idx
    assert len(test_user_from_query.teams[1].users) == 2
    assert test_user_from_query.teams[1].users[0].u_idx == test_user.u_idx
    assert test_user_from_query.teams[1].users[1].u_idx == test_user2.u_idx

def test_sns_model(api_mock_client):
    session: orm.Session = api_mock_client.app.session
    assert isinstance(session, orm.Session)

    session.query(sns.SNS).delete()
    session.commit()

    # Temporary Example
    session.add(sns.SNS(**test_sns_kwargs))

    sns_list = session.query(sns.SNS).all()
    assert len(sns_list) == 1
    assert sns_list[0].name == test_sns_kwargs['name']
    assert sns_list[0].url == test_sns_kwargs['url']

