"""empty message

Revision ID: 522ab8856717
Revises: 
Create Date: 2021-05-21 14:17:48.860857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '522ab8856717'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('food',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('worker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('worker', sa.Integer(), nullable=True),
    sa.Column('food', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['food'], ['food.id'], ),
    sa.ForeignKeyConstraint(['worker'], ['worker.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_table('worker')
    op.drop_table('food')
    # ### end Alembic commands ###
