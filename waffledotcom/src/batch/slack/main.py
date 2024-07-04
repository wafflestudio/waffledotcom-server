import asyncio

from fastapi import Depends
from loguru import logger

from waffledotcom.src.apps.user.services import UserService
from waffledotcom.src.batch.slack.services import AsyncSlackApiService
from waffledotcom.src.utils.dependency_solver import DependencySolver


async def create_users_from_slack(
    user_service: UserService = Depends(),
    slack_api_service: AsyncSlackApiService = Depends(),
):
    members_to_create = await slack_api_service.get_members()
    user_service.create_users_from_slack(members_to_create)
    logger.debug(f"Created {len(members_to_create)} users from slack")


def main():
    solver = DependencySolver()
    asyncio.run(solver.run(create_users_from_slack))


if __name__ == "__main__":
    main()
