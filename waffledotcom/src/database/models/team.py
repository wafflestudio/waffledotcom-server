import sqlalchemy as sql
from sqlalchemy.orm import relationship

from src.database.models import base as base_model


class TeamUserAssociation(base_model.BaseModel):
    __table__ = 'teams_users'

    team_id = sql.Column(sql.Integer, sql.ForeignKey('tb_team.t_idx', ondelete='CASCADE'), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('tb_user.u_idx', ondelete='CASCADE'), primary_key=True)

    team = relationship('Team', back_populates='users')
    user = relationship('User', back_populates='teams')


class Team(base_model.BaseModel):
    __tablename__ = "tb_team"

    t_idx = sql.Column(name="t_idx", type_=sql.INT, primary_key=True, autoincrement=True)
    name = sql.Column(name="name", type_=sql.VARCHAR(50), unique=True)
    users = relationship('TeamUserAssociation', back_populates='team')

