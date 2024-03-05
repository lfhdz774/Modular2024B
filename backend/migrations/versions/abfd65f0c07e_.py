"""empty message

Revision ID: abfd65f0c07e
Revises: 0b31ccba74f7
Create Date: 2024-03-04 20:26:37.768231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abfd65f0c07e'
down_revision = '0b31ccba74f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requester_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('approver_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('approver_id')
        batch_op.drop_column('requester_id')

    # ### end Alembic commands ###
