from typing import Type
from sqlalchemy import orm

DeclarativeBase: Type[orm.DeclarativeBase] = orm.declarative_base()
