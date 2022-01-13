"""add content column to posts table

Revision ID: 68c8e3102dc8
Revises: d01ba611108c
Create Date: 2022-01-12 21:06:59.271769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68c8e3102dc8'
down_revision = 'd01ba611108c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
