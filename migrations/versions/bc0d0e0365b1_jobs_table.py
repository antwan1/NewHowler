"""jobs table

Revision ID: bc0d0e0365b1
Revises: d3a4089d77b2
Create Date: 2021-10-01 14:25:29.769144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc0d0e0365b1'
down_revision = 'd3a4089d77b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobpost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('dateposted', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobpost_dateposted'), 'jobpost', ['dateposted'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_jobpost_dateposted'), table_name='jobpost')
    op.drop_table('jobpost')
    # ### end Alembic commands ###
