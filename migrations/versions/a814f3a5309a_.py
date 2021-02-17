"""empty message

Revision ID: a814f3a5309a
Revises: cb27704eacf9
Create Date: 2021-02-06 14:08:28.496426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a814f3a5309a'
down_revision = 'cb27704eacf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'role', ['role'], ['id'])
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role')
    # ### end Alembic commands ###