from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from waffledotcom.src.database.models.base import DeclarativeBase
from waffledotcom.src.database.models.base import intpk
from waffledotcom.src.database.models.base import str30
from waffledotcom.src.database.models.base import str50_default_none
from waffledotcom.src.database.models.position import position_user_association
from waffledotcom.src.database.models.team import team_user_association

if TYPE_CHECKING:
    from waffledotcom.src.database.models.position import Position
    from waffledotcom.src.database.models.sns import SNSAccount
    from waffledotcom.src.database.models.team import Team


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
