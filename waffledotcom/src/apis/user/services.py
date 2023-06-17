from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from waffledotcom.src.apis.user.exception import UserAlreadyExistsException
from waffledotcom.src.apis.user.exception import UserNotFoundException
from waffledotcom.src.apis.user.repositories import UserRepository
from waffledotcom.src.apis.user.schema import UserCreateResponse
from waffledotcom.src.apis.user.schema import UserCreateUpdateRequest
from waffledotcom.src.apis.user.schema import UserDetailResponse
from waffledotcom.src.database.models import User
from waffledotcom.src.external.slack.schema import SlackMember


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
                last_name="",
                is_member=True,
            )
            for slack_member in slack_members
        ]

        try:
            self.user_repository.create_users(users)
        except IntegrityError as exc:
            raise UserAlreadyExistsException from exc

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
