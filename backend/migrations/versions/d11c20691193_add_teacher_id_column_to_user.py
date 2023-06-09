"""Add teacher_id column to User

Revision ID: d11c20691193
Revises: 5b791911c731
Create Date: 2023-06-11 23:20:24.790262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd11c20691193'
down_revision = '5b791911c731'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app_user', sa.Column('teacher_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'app_user', 'app_user', ['teacher_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'app_user', type_='foreignkey')
    op.drop_column('app_user', 'teacher_id')
    # ### end Alembic commands ###
