"""add remaining post column

Revision ID: 80f7d1ced904
Revises: 10eb0c8e47b6
Create Date: 2026-02-26 23:05:44.309779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80f7d1ced904'
down_revision: Union[str, Sequence[str], None] = '10eb0c8e47b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts' 'published')
    op.drop_column('posts', 'created_at')
    pass
