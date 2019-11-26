"""empty message

Revision ID: 3c31137baf22
Revises: d850c5fb2cb1
Create Date: 2019-11-26 11:08:01.301442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c31137baf22'
down_revision = 'd850c5fb2cb1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('compendium', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_compendium_title', table_name='compendium')
    op.create_index(op.f('ix_compendium_title'), 'compendium', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_compendium_title'), table_name='compendium')
    op.create_index('ix_compendium_title', 'compendium', ['title'], unique=False)
    op.alter_column('compendium', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
