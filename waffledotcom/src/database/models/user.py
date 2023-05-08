import sqlalchemy as sql
from sqlalchemy.orm import relationship
import sqlalchemy_utils as sql_utils

from src.database.models import base as base_model
from src.database.models.position import position_user_association
from src.database.models.team import team_user_association


class User(base_model.DeclarativeBase):
    __tablename__ = "tb_user"

    u_idx = sql.Column(
        name="u_idx", type_=sql.INT, primary_key=True, autoincrement=True
    )
    username = sql.Column(name="username", type_=sql.VARCHAR(50), unique=True)
    password = sql.Column(
        name="password", type_=sql_utils.PasswordType(schemes=["pbkdf2_sha512"])
    )

    first_name = sql.Column(name="first_name", type_=sql.VARCHAR(50))
    last_name = sql.Column(name="last_name", type_=sql.VARCHAR(50))
    student_id = sql.Column(name="student_id", type_=sql.VARCHAR(20))

    department = sql.Column(name="department", type_=sql.VARCHAR(40))
    college = sql.Column(name="college", type_=sql.VARCHAR(40))

    phone_number = sql.Column(
        name="phone_number", type_=sql_utils.PhoneNumberType()
    )  # +821012345678
    github_id = sql.Column(name="github_id", type_=sql.VARCHAR(50))
    github_email = sql.Column(name="github_email", type_=sql_utils.EmailType)
    slack_id = sql.Column(name="slack_id", type_=sql.VARCHAR(50))
    slack_email = sql.Column(name="slack_email", type_=sql_utils.EmailType)
    notion_email = sql.Column(name="notion_email", type_=sql_utils.EmailType)
    apple_email = sql.Column(
        name="apple_email", type_=sql_utils.EmailType, nullable=True
    )

    generation = sql.Column(name="generation", type_=sql.INT)
    active = sql.Column(name="active", type_=sql.BOOLEAN)

    teams = relationship(
        "Team", secondary=team_user_association, back_populates="users"
    )
    positions = relationship(
        "Position", secondary=position_user_association, back_populates="users"
    )
    sns = relationship("SNS", back_populates="user")

    introduction = sql.Column(name="introduce", type_=sql.TEXT, nullable=True)
