from __future__ import annotations

import re
from enum import StrEnum
from urllib.parse import urlparse

from pydantic import AliasPath, BaseModel, Field, field_validator

PHONE_PATTERN = re.compile(r"^(010|011|016)\d{7,8}$")


class CustomFieldId(StrEnum):
    GITHUB_LINK = "Xf01UD0C7526"
    POSITION = "Xf01UD0AM3S6"
    GENERATION = "Xf02CN9EEQCD"


class SlackMemberProfile(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    image_192: str | None = None
    github_id: str | None = Field(
        None, validation_alias=AliasPath("fields", CustomFieldId.GITHUB_LINK, "value")
    )
    position: str | None = Field(
        None, validation_alias=AliasPath("fields", CustomFieldId.POSITION, "value")
    )
    generation: str | None = Field(
        None, validation_alias=AliasPath("fields", CustomFieldId.GENERATION, "value")
    )

    @field_validator("phone")
    @classmethod
    def check_phone_number(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.replace("-", "").replace(" ", "")
            if not PHONE_PATTERN.match(value):
                value = None
        return value

    @field_validator("github_id")
    @classmethod
    def check_github_id(cls, value: str | None) -> str | None:
        result = urlparse(value)
        assert result.scheme == "https", "Invalid URL scheme"
        assert result.netloc in ["github.com", "www.github.com"], "Invalid URL netloc"
        return str(result.path).split("/")[1]


class SlackMember(BaseModel):
    id: str
    real_name: str | None = None
    profile: SlackMemberProfile
    deleted: bool
    is_bot: bool
    is_email_confirmed: bool | None = None
    is_admin: bool | None = None


SlackMember.model_rebuild()
