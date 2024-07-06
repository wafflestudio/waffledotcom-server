import asyncio

from fastapi import Depends
from loguru import logger

from waffledotcom.src.apps.user.services import UserService
from waffledotcom.src.batch.slack.services import AsyncSlackApiService
from waffledotcom.src.utils.dependency_solver import solver


async def create_users_from_slack(
    user_service: UserService = Depends(),
    slack_api_service: AsyncSlackApiService = Depends(),
):
    members_to_create = await slack_api_service.get_members()
    for member in members_to_create:
        profile = await slack_api_service.get_profile(member.id)
        member.profile = profile
    user_service.create_or_update_users_from_slack(members_to_create)
    logger.debug(f"Created {len(members_to_create)} users from slack")


def main():
    try:
        asyncio.create_task(solver.run(create_users_from_slack))
    except RuntimeError:
        asyncio.run(solver.run(create_users_from_slack))


if __name__ == "__main__":
    main()
