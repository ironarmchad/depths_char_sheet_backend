"""empty message

Revision ID: 603c350aa50a
Revises: 3c31137baf22
Create Date: 2020-01-11 13:54:29.423163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '603c350aa50a'
down_revision = '3c31137baf22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('viewers', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('characters', 'viewers')
    # ### end Alembic commands ###
