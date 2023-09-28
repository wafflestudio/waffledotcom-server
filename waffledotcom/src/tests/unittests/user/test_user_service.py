import pytest
from fastapi import HTTPException

from waffledotcom.src.apps.user.schemas import UserCreateUpdateRequest
from waffledotcom.src.apps.user.services import UserService


def test_create_user(user_service: UserService):
    request = UserCreateUpdateRequest(
        sso_id="test",
        username="test",
        first_name="test",
        last_name="test",
    )
    response = user_service.create_user(request)
    assert response.id is not None


def test_create_user_duplicate_username(user_service: UserService):
    request = UserCreateUpdateRequest(
        sso_id="test",
        username="test",
        first_name="test",
        last_name="test",
    )
    user_service.create_user(request)
    with pytest.raises(HTTPException) as excinfo:
        new_request = request.copy()
        new_request.sso_id = "test2"
        user_service.create_user(new_request)
        assert excinfo.value.status_code == 409


def test_create_user_duplicate_sso_id(user_service: UserService):
    request = UserCreateUpdateRequest(
        sso_id="test",
        username="test",
        first_name="test",
        last_name="test",
    )
    user_service.create_user(request)
    with pytest.raises(HTTPException) as excinfo:
        new_request = request.copy()
        new_request.username = "test2"
        user_service.create_user(new_request)
        assert excinfo.value.status_code == 409


def test_list_user_detail(user_service: UserService):
    request = UserCreateUpdateRequest(
        sso_id="test",
        username="test",
        first_name="test",
        last_name="test",
    )
    response = user_service.create_user(request)
    assert response.id is not None

    users = user_service.list_users()
    assert len(users) == 1
    assert users[0].id == response.id
    assert users[0].sso_id == request.sso_id
