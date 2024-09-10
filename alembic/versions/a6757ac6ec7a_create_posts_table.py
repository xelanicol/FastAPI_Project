"""Create posts table

Revision ID: a6757ac6ec7a
Revises: 
Create Date: 2024-09-10 12:35:50.989294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6757ac6ec7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(), nullable=False, primary_key=True), sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
