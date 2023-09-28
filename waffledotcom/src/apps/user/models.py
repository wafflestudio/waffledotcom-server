from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from waffledotcom.src.apps.team.models import team_user_association
from waffledotcom.src.database.base import (
    DeclarativeBase,
    intpk,
    str30,
    str50_default_none,
)

if TYPE_CHECKING:
    from waffledotcom.src.apps.team.models import Team

position_user_association = Table(
    "position_user_association",
    DeclarativeBase.metadata,
    Column(
        "position_id",
        Integer,
        ForeignKey("position.id"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id"),
        primary_key=True,
    ),
)


class User(DeclarativeBase):
    __tablename__ = "user"

    id: Mapped[intpk]
    sso_id: Mapped[str50_default_none] = mapped_column(unique=True)
    username: Mapped[str50_default_none] = mapped_column(unique=True)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)

    first_name: Mapped[str30]
    last_name: Mapped[str30]

    department: Mapped[str50_default_none]
    college: Mapped[str50_default_none]

    phone_number: Mapped[str30 | None]

    github_id: Mapped[str50_default_none]
    github_email: Mapped[str50_default_none]
    slack_id: Mapped[str50_default_none] = mapped_column(unique=True)
    slack_email: Mapped[str50_default_none]
    notion_email: Mapped[str50_default_none]
    apple_email: Mapped[str50_default_none]

    is_rookie: Mapped[bool] = mapped_column(Boolean, default=False)
    is_member: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    introduction: Mapped[str] = mapped_column(String(1000), nullable=True)

    teams: Mapped[list["Team"]] = relationship(
        secondary=team_user_association, back_populates="users"
    )
    positions: Mapped[list["Position"]] = relationship(
        secondary=position_user_association, back_populates="users"
    )
    sns_accounts: Mapped[list["SNSAccount"]] = relationship(
        back_populates="user", cascade="all, delete"
    )


class Position(DeclarativeBase):
    __tablename__ = "position"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), unique=True)
    users: Mapped[list["User"]] = relationship(
        secondary=position_user_association, back_populates="positions"
    )


class SNSAccount(DeclarativeBase):
    __tablename__ = "sns_account"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
    )
    user: Mapped["User"] = relationship(back_populates="sns_accounts")
    name: Mapped[str30]
    url: Mapped[str] = mapped_column(String(200))
