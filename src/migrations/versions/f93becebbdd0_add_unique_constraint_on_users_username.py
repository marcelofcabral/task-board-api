"""add unique constraint on users.username

Revision ID: f93becebbdd0
Revises: d3e2af3482cc
Create Date: 2026-06-22 19:20:40.754001

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f93becebbdd0"
down_revision: Union[str, Sequence[str], None] = "d3e2af3482cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("users", recreate="auto") as batch_op:
        batch_op.create_unique_constraint("uq_users_username", ["username"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users", recreate="auto") as batch_op:
        batch_op.drop_constraint("uq_users_username", type_="unique")
