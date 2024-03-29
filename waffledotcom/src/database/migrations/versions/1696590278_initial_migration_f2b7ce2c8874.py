"""Initial Migration

Revision ID: f2b7ce2c8874
Revises:
Create Date: 2023-10-06 20:04:38.514945

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f2b7ce2c8874"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "position",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "team",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("introduction", sa.String(length=1000), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sso_id", sa.String(length=50), nullable=True),
        sa.Column("username", sa.String(length=50), nullable=True),
        sa.Column("image_url", sa.String(length=200), nullable=True),
        sa.Column("first_name", sa.String(length=30), nullable=False),
        sa.Column("last_name", sa.String(length=30), nullable=False),
        sa.Column("department", sa.String(length=50), nullable=True),
        sa.Column("college", sa.String(length=50), nullable=True),
        sa.Column("phone_number", sa.String(length=30), nullable=True),
        sa.Column("github_id", sa.String(length=50), nullable=True),
        sa.Column("github_email", sa.String(length=50), nullable=True),
        sa.Column("slack_id", sa.String(length=50), nullable=True),
        sa.Column("slack_email", sa.String(length=50), nullable=True),
        sa.Column("notion_email", sa.String(length=50), nullable=True),
        sa.Column("apple_email", sa.String(length=50), nullable=True),
        sa.Column("is_rookie", sa.Boolean(), nullable=False),
        sa.Column("is_member", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("introduction", sa.String(length=1000), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slack_id"),
        sa.UniqueConstraint("sso_id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "position_user_association",
        sa.Column("position_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["position_id"],
            ["position.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("position_id", "user_id"),
    )
    op.create_table(
        "sns_account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("url", sa.String(length=200), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "team_user_association",
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["team.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("team_id", "user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("team_user_association")
    op.drop_table("sns_account")
    op.drop_table("position_user_association")
    op.drop_table("user")
    op.drop_table("team")
    op.drop_table("position")
    # ### end Alembic commands ###
