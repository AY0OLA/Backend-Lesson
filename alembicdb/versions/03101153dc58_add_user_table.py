"""add user table

Revision ID: 03101153dc58
Revises: 6b0f8cac7b3e
Create Date: 2026-02-26 22:38:28.663601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03101153dc58'
down_revision: Union[str, Sequence[str], None] = '6b0f8cac7b3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("user", sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user')
    pass
