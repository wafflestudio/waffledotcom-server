import pytest

from waffledotcom.src.database.models.position import Position
from waffledotcom.src.database.models.sns import SNSAccount
from waffledotcom.src.database.models.team import Team
from waffledotcom.src.database.models.user import User


@pytest.fixture
def user() -> User:
    return User(
        username="testuser",
        password="testpassword",
        first_name="Test",
        last_name="User",
        is_active_member=True,
        is_admin=False,
    )


@pytest.fixture
def team() -> Team:
    return Team(name="Test Team", introduction="This is a test team.")


@pytest.fixture
def position() -> Position:
    return Position(name="Test Position")


@pytest.fixture
def sns_account(user: User) -> SNSAccount:
    return SNSAccount(name="Test SNS", url="https://test-sns.com", user=user)
