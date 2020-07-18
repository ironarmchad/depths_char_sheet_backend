"""empty message

Revision ID: 07fe8162eb11
Revises: 603c350aa50a
Create Date: 2020-01-30 11:00:14.346911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07fe8162eb11'
down_revision = '603c350aa50a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('info', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'info')
    # ### end Alembic commands ###