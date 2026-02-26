"""add content column to post table

Revision ID: 6b0f8cac7b3e
Revises: b77534082ab4
Create Date: 2026-02-26 22:26:46.925189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b0f8cac7b3e'
down_revision: Union[str, Sequence[str], None] = 'b77534082ab4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
