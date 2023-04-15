import sqlalchemy as sql

from src.database.models import base as base_model


class User(base_model.DeclarativeBase):
    __tablename__ = "tb_user"

    id = sql.Column(name="id", type_=sql.INT, primary_key=True, autoincrement=True)
    name = sql.Column(name="name", type_=sql.VARCHAR(50))
