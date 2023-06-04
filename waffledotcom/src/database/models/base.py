from typing import Annotated, Type

from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import DeclarativeBase as Base
from sqlalchemy.orm import mapped_column

DeclarativeBase: Type[Base] = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str50 = Annotated[str, mapped_column(String(50))]
str20 = Annotated[str, mapped_column(String(20))]
