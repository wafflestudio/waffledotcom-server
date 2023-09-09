from __future__ import annotations

from pydantic import BaseModel


class SlackMember(BaseModel):
    id: str
    real_name: str | None
    profile: SlackMemberProfile
    deleted: bool
    is_bot: bool
    is_email_confirmed: bool | None
    is_admin: bool | None


class SlackMemberProfile(BaseModel):
    first_name: str | None
    last_name: str | None
    email: str | None
    image_192: str | None


SlackMember.update_forward_refs()
