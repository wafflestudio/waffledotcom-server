from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from waffledotcom.src.database.models import base as base_model
from waffledotcom.src.database.models.base import intpk
from waffledotcom.src.database.models.base import mapped_column
from waffledotcom.src.database.models.base import str20

if TYPE_CHECKING:
    from waffledotcom.src.database.models.user import User


class SNSAccount(base_model.DeclarativeBase):
    __tablename__ = "sns_account"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
    )
    user: Mapped["User"] = relationship(back_populates="sns_accounts")
    name: Mapped[str20]
    url: Mapped[str] = mapped_column(String(200))
