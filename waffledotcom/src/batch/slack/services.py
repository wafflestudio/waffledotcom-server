import asyncio
from collections.abc import Callable
from typing import Any, Coroutine

from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from waffledotcom.src.batch.slack.config import slack_config
from waffledotcom.src.batch.slack.schema import SlackMember, SlackMemberProfile


class AsyncSlackApiService:
    def __init__(self) -> None:
        self.client = AsyncWebClient(token=slack_config.token)

    async def get_members(self) -> list[SlackMember]:
        resp = await self.call_api_with_retry(self.client.users_list)

        if not resp.get("ok", False) or "members" not in resp:
            raise SlackApiError("Slack API Error", resp.data)

        members = [
            SlackMember(**member)
            for member in resp.get("members", [])
            if not member["is_bot"]
            and not member["deleted"]
            and member["id"] != "USLACKBOT"
        ]

        return members

    async def get_profile(self, user_key: str) -> SlackMemberProfile:
        resp = await self.call_api_with_retry(
            self.client.users_profile_get,
            kwargs={"user": user_key},
        )

        if not resp.get("ok", False) or "profile" not in resp:
            raise SlackApiError("Slack API Error", resp.data)

        profile = SlackMemberProfile(**resp.get("profile", {}))

        return profile

    async def call_api_with_retry(
        self,
        f: Callable[..., Coroutine[Any, Any, AsyncSlackResponse]],
        *,
        retry: int = 10,
        args: list[Any] = [],
        kwargs: dict[str, Any] = {},
    ) -> AsyncSlackResponse:
        if getattr(self.client, f.__name__, None) != f:
            raise AttributeError(f"{f} is not a method of WebClient")

        exc = Exception("이게 실행된다면 버그이다.")

        for _ in range(retry):
            try:
                response = await f(*args, **kwargs)
                return response
            except Exception as e:
                exc = e
                await asyncio.sleep(10)

        raise exc
