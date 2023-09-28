from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import APIKeyHeader

from waffledotcom.src.apps.user.exceptions import UserPermissionDeniedException
from waffledotcom.src.apps.user.models import User
from waffledotcom.src.apps.user.repositories import UserRepository


def get_current_user(
    waffle_user_id: Annotated[
        str,
        Security(
            APIKeyHeader(
                name="waffle-user-id",
                scheme_name="waffle-user-id",
                description=(
                    "와플스튜디오 SSO를 통해 발급받은 액세스 토큰에 포함된 사용자의"
                    " 고유 식별자입니다. "
                    "액세스 토큰을 디코드하면 확인할 수 있습니다."
                ),
            )
        ),
    ],
    user_repository: Annotated[UserRepository, Depends()],
) -> User:
    user = user_repository.get_user_by_sso_id(waffle_user_id)
    if user is None:
        raise UserPermissionDeniedException
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_admin_user(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise UserPermissionDeniedException
    return current_user


AdminUser = Annotated[User, Depends(get_admin_user)]
