"""create books table

Revision ID: e305359b6ffa
Revises: 
Create Date: 2026-09-22 17:24:42.936798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e305359b6ffa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('author', sa.String(length=100), nullable=False),
        sa.Column('publication_date', sa.Date(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=False)
    op.create_index(op.f('ix_books_author'), 'books', ['author'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_books_author'), table_name='books')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_table('books')
