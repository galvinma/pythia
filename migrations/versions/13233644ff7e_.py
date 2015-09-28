"""empty message

Revision ID: 13233644ff7e
Revises: None
Create Date: 2015-09-27 17:56:59.095871

"""

# revision identifiers, used by Alembic.
revision = '13233644ff7e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Login',
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('username_email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('first_name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Login')
    ### end Alembic commands ###
