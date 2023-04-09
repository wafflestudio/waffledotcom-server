import sqlalchemy as sql
from sqlalchemy.orm import relationship

from src.database.models import base as base_model


class PositionUserAssociation(base_model.BaseModel):
    __table__ = 'positions_users'

    position_id = sql.Column(sql.Integer, sql.ForeignKey('tb_position.p_idx', ondelete='CASCADE'), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('tb_user.u_idx', ondelete='CASCADE'), primary_key=True)

    position = relationship('Position', back_populates='users')
    user = relationship('User', back_populates='teams')


class Position(base_model.BaseModel):
    __tablename__ = "tb_position"

    p_idx = sql.Column(name="p_idx", type_=sql.INT, primary_key=True, autoincrement=True)
    name = sql.Column(name="name", type_=sql.VARCHAR(50), unique=True)
    users = relationship('PositionUserAssociation', back_populates='position')

