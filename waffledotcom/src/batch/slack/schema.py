from __future__ import annotations

from pydantic import BaseModel


class SlackMember(BaseModel):
    id: str
    real_name: str | None = None
    profile: SlackMemberProfile
    deleted: bool
    is_bot: bool
    is_email_confirmed: bool | None = None
    is_admin: bool | None = None


class SlackMemberProfile(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    image_192: str | None = None


SlackMember.model_rebuild()
