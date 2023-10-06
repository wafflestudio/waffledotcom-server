import asyncio
import json
import pickle

from devtools import debug
from fastapi import Depends
from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from waffledotcom.src.apps.user.services import UserService
from waffledotcom.src.batch.slack.config import slack_config
from waffledotcom.src.batch.slack.schema import SlackMember
from waffledotcom.src.utils.dependency_solver import DependencySolver


async def create_users_from_slack(user_service: UserService = Depends()):
    if not slack_config.token:
        raise ValueError(
            "Slack token is not set. Please check your environment variables."
        )

    client = WebClient(token=slack_config.token)
    data = client.users_list().data

    assert isinstance(data, dict)

    # store data as json file
    with open("./users_list.json", "w") as f:
        json.dump(data, f)

    if not data.get("ok", False):
        raise SlackApiError("Slack API Error", data)

    members_to_create = []
    for member in data.get("members", []):
        if member["is_bot"] or member["deleted"] or member["id"] == "USLACKBOT":
            continue

        member = SlackMember(**member)
        members_to_create.append(member)

    # pickle members_to_create
    with open("./members_to_create.pickle", "wb") as f:
        pickle.dump(members_to_create, f)

    debug(members_to_create)
    # user_service.create_users_from_slack(members_to_create)
    logger.debug(f"Created {len(members_to_create)} users from slack")


def main():
    solver = DependencySolver()
    asyncio.run(solver.run(create_users_from_slack))


if __name__ == "__main__":
    main()
