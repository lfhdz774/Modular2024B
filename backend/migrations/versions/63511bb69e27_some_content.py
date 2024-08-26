"""Some content

Revision ID: 63511bb69e27
Revises: 83e72127c956
Create Date: 2024-08-26 14:00:09.470614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63511bb69e27'
down_revision = '83e72127c956'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('group_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('group_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('server_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['server_id'], ['servers.server_id'], name='group_server_id_fkey'),
    sa.PrimaryKeyConstraint('group_id', name='group_pkey')
    )
    # ### end Alembic commands ###
