from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from waffledotcom.src.database.base import DeclarativeBase, intpk, str30

if TYPE_CHECKING:
    from waffledotcom.src.apps.user.models import User

team_user_association = Table(
    "team_user_association",
    DeclarativeBase.metadata,
    Column(
        "team_id",
        Integer,
        ForeignKey("team.id"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id"),
        primary_key=True,
    ),
)


class Team(DeclarativeBase):
    __tablename__ = "team"

    id: Mapped[intpk]
    name: Mapped[str30]
    introduction: Mapped[str] = mapped_column(String(1000), nullable=True)
    users: Mapped[list["User"]] = relationship(
        secondary=team_user_association,
        back_populates="teams",
    )
