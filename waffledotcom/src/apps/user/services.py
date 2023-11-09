from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from waffledotcom.src.apps.user.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from waffledotcom.src.apps.user.models import User
from waffledotcom.src.apps.user.repositories import UserRepository
from waffledotcom.src.apps.user.schemas import (
    UserCreateResponse,
    UserCreateUpdateRequest,
    UserDetailResponse,
)
from waffledotcom.src.batch.slack.schema import SlackMember


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository

    def create_user(self, request: UserCreateUpdateRequest) -> UserCreateResponse:
        if request.sso_id is None:
            raise HTTPException(status_code=400, detail="SSO ID가 필요합니다.")
        user = User(
            sso_id=request.sso_id,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            positions=request.positions,
            department=request.department,
            college=request.college,
            phone_number=request.phone_number,
            github_id=request.github_id,
            github_email=request.github_email,
            slack_id=request.slack_id,
            slack_email=request.slack_email,
            notion_email=request.notion_email,
            apple_email=request.apple_email,
            introduction=request.introduction,
        )
        try:
            user = self.user_repository.create_user(user)
        except IntegrityError as exc:
            raise UserAlreadyExistsException from exc
        return UserCreateResponse.from_orm(user)

    def create_users_from_slack(self, slack_members: list[SlackMember]) -> None:
        users = [
            User(
                image_url=slack_member.profile.image_192,
                slack_id=slack_member.id,
                slack_email=slack_member.profile.email,
                first_name=slack_member.real_name or "",
                phone_number=slack_member.profile.phone or None,
                last_name="",
                is_member=True,
            )
            for slack_member in slack_members
        ]

        for user in users:
            assert isinstance(user.slack_id, str)
            if (
                created_user := self.user_repository.get_user_by_slack_id(user.slack_id)
            ) is None:
                self.user_repository.create_user(user)
                continue

            created_user.slack_email = user.slack_email
            created_user.phone_number = user.phone_number
            created_user.image_url = user.image_url
            created_user.first_name = user.first_name
            created_user.last_name = user.last_name
            self.user_repository.update_user(created_user)

    def update_user(
        self, user_id: int, request: UserCreateUpdateRequest
    ) -> UserDetailResponse:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException

        user = self.user_repository.update_user(user)
        if user is None:
            raise UserNotFoundException

        return UserDetailResponse.from_orm(user)

    def list_users(self) -> list[UserDetailResponse]:
        users = self.user_repository.get_users()
        return [UserDetailResponse.from_orm(user) for user in users]
