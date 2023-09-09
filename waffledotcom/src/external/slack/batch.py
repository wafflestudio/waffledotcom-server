import asyncio
import pickle

from fastapi import Depends
from loguru import logger
from slack_sdk.errors import SlackApiError

from waffledotcom.src.apis.user.services import UserService
from waffledotcom.src.external.slack.schema import SlackMember
from waffledotcom.src.utils.dependency_solver import DependencySolver


async def create_users_from_slack(user_service: UserService = Depends()):
    with open("response.pickle", "rb") as f:
        response = pickle.load(f)
        data = response.data

    # Uncomment this to get data from slack
    # client = WebClient(token="")
    # assert isinstance(data := client.users_list().data, dict)

    if not data.get("ok", False):
        raise SlackApiError("Slack API Error", response)

    members_to_create = []
    for member in data.get("members", []):
        member = SlackMember(**member)

        if member.is_bot or member.deleted or member.id == "USLACKBOT":
            continue

        members_to_create.append(member)
    user_service.create_users_from_slack(members_to_create)
    logger.debug(f"Created {len(members_to_create)} users from slack")


def main():
    solver = DependencySolver()
    asyncio.run(solver.run(create_users_from_slack))


if __name__ == "__main__":
    main()
