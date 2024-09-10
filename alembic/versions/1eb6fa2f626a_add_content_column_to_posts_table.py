"""add content column to posts table

Revision ID: 1eb6fa2f626a
Revises: a6757ac6ec7a
Create Date: 2024-09-10 12:45:18.732999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eb6fa2f626a'
down_revision: Union[str, None] = 'a6757ac6ec7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
