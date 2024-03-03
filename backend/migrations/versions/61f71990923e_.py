"""empty message

Revision ID: 61f71990923e
Revises: aa311edfdad6
Create Date: 2024-03-03 00:31:30.710111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61f71990923e'
down_revision = 'aa311edfdad6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('requester_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('approver_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('approver_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('requester_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
