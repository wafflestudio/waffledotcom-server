from sqlalchemy import orm
from sqlalchemy.ext import declarative

BaseModel: orm.DeclarativeBase = declarative.declarative_base()
