import sqlalchemy as sql
from sqlalchemy.orm import relationship

from waffledotcom.src.database.models import base as base_model

position_user_association = sql.Table(
    "positions_users",
    base_model.DeclarativeBase.metadata,
    sql.Column(
        "position_id",
        sql.Integer,
        sql.ForeignKey("tb_position.p_idx", ondelete="CASCADE"),
        primary_key=True,
    ),
    sql.Column(
        "user_id",
        sql.Integer,
        sql.ForeignKey("tb_user.u_idx", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Position(base_model.DeclarativeBase):
    __tablename__ = "tb_position"

    p_idx = sql.Column(
        name="p_idx", type_=sql.INT, primary_key=True, autoincrement=True
    )
    name = sql.Column(name="name", type_=sql.VARCHAR(50), unique=True)
    users = relationship(
        "User", secondary=position_user_association, back_populates="positions"
    )
