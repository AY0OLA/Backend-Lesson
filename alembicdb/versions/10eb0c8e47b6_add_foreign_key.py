"""add foreign key

Revision ID: 10eb0c8e47b6
Revises: 03101153dc58
Create Date: 2026-02-26 22:51:17.236598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10eb0c8e47b6'
down_revision: Union[str, Sequence[str], None] = '03101153dc58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table="posts", referent_table="user", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
