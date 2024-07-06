import pytest

from waffledotcom.src.apps.team.models import Team
from waffledotcom.src.apps.user.models import Position, SNSAccount, User


@pytest.fixture
def user() -> User:
    return User(
        sso_id="abcdef123",
        username="testuser",
        first_name="Test",
        last_name="User",
        is_active=True,
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
