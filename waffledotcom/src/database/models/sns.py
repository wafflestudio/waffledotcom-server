import sqlalchemy as sql
from sqlalchemy.orm import relationship

from src.database.models import base as base_model


class SNS(base_model.BaseModel):
    __tablename__ = "tb_sns"

    s_idx = sql.Column(name="s_idx", type_=sql.INT, primary_key=True, autoincrement=True)
    u_idx = sql.Column(sql.INT, sql.ForeignKey('tb_user.u_idx', ondelete='CASCADE'), name="u_idx")
    name = sql.Column(name="name", type_=sql.VARCHAR(50), unique=True)
    url = sql.Column(name="url", type_=sql.VARCHAR(100))