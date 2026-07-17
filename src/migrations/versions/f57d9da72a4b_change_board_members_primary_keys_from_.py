"""change board members primary keys from id to board_id and user_id

Revision ID: f57d9da72a4b
Revises: 3260cb28c177
Create Date: 2026-06-30 19:11:23.064505

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f57d9da72a4b"
down_revision: Union[str, Sequence[str], None] = "3260cb28c177"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _create_board_members_table(table_name: str) -> None:
    op.create_table(
        table_name,
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.PrimaryKeyConstraint("user_id", "board_id"),
    )


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("board_members"):
        _create_board_members_table("board_members")
        return

    columns = {column["name"] for column in inspector.get_columns("board_members")}
    if "id" not in columns:
        return

    _create_board_members_table("board_members_new")
    op.execute(
        """
        INSERT INTO board_members_new (user_id, board_id, role)
        SELECT user_id, board_id, role FROM board_members
        """
    )
    op.drop_table("board_members")
    op.rename_table("board_members_new", "board_members")


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table("board_members", "board_members_old")
    op.create_table(
        "board_members",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_board_members_id"), "board_members", ["id"], unique=False)
    op.create_index(
        op.f("ix_board_members_user_id"), "board_members", ["user_id"], unique=False
    )
    op.create_index(
        op.f("ix_board_members_board_id"), "board_members", ["board_id"], unique=False
    )
    op.execute(
        """
        INSERT INTO board_members (user_id, board_id, role)
        SELECT user_id, board_id, role FROM board_members_old
        """
    )
    op.drop_table("board_members_old")
