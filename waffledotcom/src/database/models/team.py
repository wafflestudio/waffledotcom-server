import sqlalchemy as sql
from sqlalchemy.orm import relationship

from src.database.models import base as base_model

team_user_association = sql.Table(
    'teams_users',
    base_model.BaseModel.metadata,
    sql.Column('team_id', sql.Integer, sql.ForeignKey('tb_team.t_idx', ondelete='CASCADE'), primary_key=True),
    sql.Column('user_id', sql.Integer, sql.ForeignKey('tb_user.u_idx', ondelete='CASCADE'), primary_key=True)
)


class Team(base_model.BaseModel):
    __tablename__ = "tb_team"

    t_idx = sql.Column(name="t_idx", type_=sql.INT, primary_key=True, autoincrement=True)
    name = sql.Column(name="name", type_=sql.VARCHAR(50), unique=True)
    introduction = sql.Column(name="introduce", type_=sql.TEXT, nullable=True)
    users = relationship('User', secondary=team_user_association, back_populates='teams')

