"""Some content

Revision ID: 83e72127c956
Revises: 0de79931057d
Create Date: 2024-08-26 13:57:36.949859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83e72127c956'
down_revision = '0de79931057d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('server_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['server_id'], ['servers.server_id'], ),
    sa.PrimaryKeyConstraint('group_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group')
    # ### end Alembic commands ###
