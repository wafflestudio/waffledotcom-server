import pytest
from sqlalchemy.orm import Session

from waffledotcom.src.apps.user.models import User
from waffledotcom.src.apps.user.repositories import UserRepository
from waffledotcom.src.apps.user.services import UserService
from waffledotcom.src.database.connection import Transaction


@pytest.fixture
def user() -> User:
    return User(
        sso_id="abcdef123",
        username="testuser",
        password="testpassword",
        first_name="Test",
        last_name="User",
        is_active=True,
        is_admin=False,
    )


@pytest.fixture
def user_repository(db_session: Session):
    return UserRepository(session=db_session, transaction=Transaction(db_session))


@pytest.fixture
def user_service(user_repository: UserRepository):
    return UserService(user_repository=user_repository)
