from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from waffledotcom.src.database.models.base import DeclarativeBase
from waffledotcom.src.database.models.base import intpk
from waffledotcom.src.database.models.base import str20
from waffledotcom.src.database.models.base import str50
from waffledotcom.src.database.models.position import position_user_association
from waffledotcom.src.database.models.team import team_user_association

if TYPE_CHECKING:
    from waffledotcom.src.database.models.position import Position
    from waffledotcom.src.database.models.sns import SNSAccount
    from waffledotcom.src.database.models.team import Team


class User(DeclarativeBase):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    first_name: Mapped[str20]
    last_name: Mapped[str20]

    department: Mapped[str50 | None]
    college: Mapped[str50 | None]

    phone_number: Mapped[str20 | None]

    github_id: Mapped[str50 | None]
    github_email: Mapped[str50 | None]
    slack_id: Mapped[str50 | None]
    slack_email: Mapped[str50 | None]
    notion_email: Mapped[str50 | None]
    apple_email: Mapped[str50 | None]

    is_active_member: Mapped[bool] = mapped_column(Boolean, default=False)
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
