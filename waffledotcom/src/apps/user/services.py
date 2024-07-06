from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from waffledotcom.src.apps.user.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from waffledotcom.src.apps.user.models import User
from waffledotcom.src.apps.user.repositories import UserRepository
from waffledotcom.src.apps.user.schemas import (
    SimpleUserResponse,
    UserCreateResponse,
    UserCreateUpdateRequest,
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

    def create_or_update_users_from_slack(
        self, slack_members: list[SlackMember]
    ) -> None:
        for slack_member in slack_members:
            self.create_or_update_user_from_slack(slack_member)

    def create_or_update_user_from_slack(self, slack_member: SlackMember) -> None:
        deleted_or_not_certified = (
            slack_member.deleted
            or slack_member.is_bot
            or not slack_member.is_email_confirmed
        )

        if deleted_or_not_certified:
            return

        user = self.user_repository.get_user_by_slack_id(slack_member.id)

        if user is None:
            user = User(
                slack_id=slack_member.id,
                first_name=slack_member.profile.first_name or "",
                last_name=slack_member.profile.last_name or "",
                slack_email=slack_member.profile.email,
                phone_number=slack_member.profile.phone or None,
                image_url=slack_member.profile.image_192,
                github_id=slack_member.profile.github_id,
                # 추후 DB의 Position 테이블과 정합성 맞춘 후 추가
                # position=slack_member.profile.position,
                generation=slack_member.profile.generation,
                is_member=True,
            )
            self.user_repository.create_user(user)
        else:
            user.first_name = slack_member.profile.first_name or user.first_name
            user.last_name = slack_member.profile.last_name or user.last_name
            user.slack_email = slack_member.profile.email or user.slack_email
            user.phone_number = slack_member.profile.phone or user.phone_number
            user.image_url = slack_member.profile.image_192 or user.image_url
            user.github_id = slack_member.profile.github_id or user.github_id
            # user.position = slack_member.profile.position or user.position
            user.generation = slack_member.profile.generation or user.generation
            user.is_member = True
            self.user_repository.update_user(user)

    def update_user(
        self, user_id: int, request: UserCreateUpdateRequest
    ) -> SimpleUserResponse:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException

        user = self.user_repository.update_user(user)
        if user is None:
            raise UserNotFoundException

        return SimpleUserResponse.from_orm(user)

    def list_users(self) -> list[SimpleUserResponse]:
        users = self.user_repository.get_users()
        return [SimpleUserResponse.from_orm(user) for user in users]
