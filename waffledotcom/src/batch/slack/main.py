import asyncio

from fastapi import Depends
from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from waffledotcom.src.apps.user.services import UserService
from waffledotcom.src.batch.slack.config import slack_config
from waffledotcom.src.batch.slack.schema import SlackMember
from waffledotcom.src.utils.dependency_solver import DependencySolver


async def create_users_from_slack(user_service: UserService = Depends()):
    client = WebClient(token=slack_config.token)
    data = client.users_list().data

    assert isinstance(data, dict)

    if not data.get("ok", False):
        raise SlackApiError("Slack API Error", data)

    members_to_create = []
    for member in data.get("members", []):
        if member["is_bot"] or member["deleted"] or member["id"] == "USLACKBOT":
            continue

        member = SlackMember(**member)
        if member.profile.phone is not None:
            phone = (
                member.profile.phone.replace("-", "")
                .replace(" ", "")
                .replace("+82", "")
            )
            member.profile.phone = phone

        members_to_create.append(member)

    user_service.create_users_from_slack(members_to_create)
    logger.debug(f"Created {len(members_to_create)} users from slack")


def main():
    solver = DependencySolver()
    asyncio.run(solver.run(create_users_from_slack))


if __name__ == "__main__":
    main()
