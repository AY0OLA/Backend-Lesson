"""create posts table

Revision ID: b77534082ab4
Revises:
Create Date: 2026-02-26 20:37:44.083245
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b77534082ab4"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")