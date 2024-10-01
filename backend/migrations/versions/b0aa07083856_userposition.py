"""userPosition

Revision ID: b0aa07083856
Revises: a58eeaf6f8d5
Create Date: 2024-09-30 14:04:34.485536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0aa07083856'
down_revision = 'a58eeaf6f8d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('positions',
        sa.Column('position_id', sa.Integer(), nullable=False),
        sa.Column('position_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('position_id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('employee_position', sa.Integer(), nullable=True))
        
    # Set a default value for existing rows
    op.execute("UPDATE users SET employee_position = 1 WHERE employee_position IS NULL")
    
    # Alter the column to set it as NOT NULL
    op.alter_column('users', 'employee_position', nullable=False)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('employee_position')

    op.drop_table('positions')
    # ### end Alembic commands ###
