from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from waffledotcom.src.database.models.base import DeclarativeBase
from waffledotcom.src.database.models.base import intpk
from waffledotcom.src.database.models.base import mapped_column

if TYPE_CHECKING:
    from waffledotcom.src.database.models.user import User

position_user_association = Table(
    "positions_users",
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


class Position(DeclarativeBase):
    __tablename__ = "position"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), unique=True)
    users: Mapped[list["User"]] = relationship(
        secondary=position_user_association, back_populates="positions"
    )
