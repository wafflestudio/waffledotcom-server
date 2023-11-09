from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase as Base
from sqlalchemy.orm import declarative_base, mapped_column

DeclarativeBase: type[Base] = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str30 = Annotated[str, mapped_column(String(30))]
str50 = Annotated[str, mapped_column(String(50))]
str255 = Annotated[str, mapped_column(String(255))]
str50_default_none = Annotated[
    str | None,
    mapped_column(String(50), nullable=True, default=None),
]
