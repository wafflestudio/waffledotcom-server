from typing import Annotated

from fastapi import APIRouter, Depends, Header

from waffledotcom.src.apps.user.dependencies import CurrentUser
from waffledotcom.src.apps.user.exceptions import UserPermissionDeniedException
from waffledotcom.src.apps.user.schemas import UserCreateUpdateRequest
from waffledotcom.src.apps.user.services import UserService

v1_router = APIRouter(prefix="/v1/users", tags=["users"])


@v1_router.post("")
def create_user(
    request: UserCreateUpdateRequest,
    waffle_user_id: Annotated[str, Header()],
    user_service: UserService = Depends(),
):
    request.sso_id = waffle_user_id
    return user_service.create_user(request)


@v1_router.patch("/{user_id}")
def update_user(
    user_id: int,
    request: UserCreateUpdateRequest,
    current_user: CurrentUser,
    user_service: UserService = Depends(),
):
    if not (current_user.id == user_id or current_user.is_admin):
        raise UserPermissionDeniedException
    return user_service.update_user(user_id, request)


@v1_router.get("")
def list_users(
    user_service: UserService = Depends(),
    # current_user: User = Depends(get_current_user),
):
    # if not current_user.is_admin:
    #     raise UserPermissionDeniedException
    return user_service.list_users()
