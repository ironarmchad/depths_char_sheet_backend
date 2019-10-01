"""empty message

Revision ID: 718f0e04b62f
Revises: 658916aff098
Create Date: 2019-09-10 09:13:11.853792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '718f0e04b62f'
down_revision = '658916aff098'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('characters', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.drop_index('ix_characters_name', table_name='characters')
    op.create_index(op.f('ix_characters_name'), 'characters', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_characters_name'), table_name='characters')
    op.create_index('ix_characters_name', 'characters', ['name'], unique=True)
    op.alter_column('characters', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###