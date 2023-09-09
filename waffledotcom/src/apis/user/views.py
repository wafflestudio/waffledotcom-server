from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Security
from fastapi.security import APIKeyHeader

from waffledotcom.src.apis.user.exception import UserPermissionDeniedException
from waffledotcom.src.apis.user.repositories import UserRepository
from waffledotcom.src.apis.user.schema import UserCreateUpdateRequest
from waffledotcom.src.apis.user.services import UserService
from waffledotcom.src.database.models.user import User

v1_router = APIRouter(prefix="/v1/users", tags=["users"])


def get_current_user(
    waffle_user_id: str = Security(
        APIKeyHeader(
            name="waffle-user-id",
            scheme_name="waffle-user-id",
            description=(
                "와플스튜디오 SSO를 통해 발급받은 액세스 토큰에 포함된 사용자의 고유 식별자입니다. "
                "액세스 토큰을 디코드하면 확인할 수 있습니다."
            ),
        )
    ),
    user_repository: UserRepository = Depends(),
) -> User:
    user = user_repository.get_user_by_sso_id(waffle_user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")
    return user


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
    user_service: UserService = Depends(),
    current_user: User = Depends(get_current_user),
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
