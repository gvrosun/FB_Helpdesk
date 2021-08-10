"""Added facebook user.

Revision ID: 34fd9ce57f7e
Revises: 16a6da1adbd3
Create Date: 2021-08-10 11:16:05.386182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34fd9ce57f7e'
down_revision = '16a6da1adbd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flask_dance_oauth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('token', sa.JSON(), nullable=False),
    sa.Column('provider_user_id', sa.String(length=256), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flask_dance_oauth')
    # ### end Alembic commands ###