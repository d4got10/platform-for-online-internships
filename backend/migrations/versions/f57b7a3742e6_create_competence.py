"""Create Competence

Revision ID: f57b7a3742e6
Revises: dd8cab8d69f5
Create Date: 2023-05-23 14:08:42.126439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f57b7a3742e6'
down_revision = '431b1df01c98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_competence',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_competence_id'), 'app_competence', ['id'], unique=True)
    op.create_index(op.f('ix_app_competence_name'), 'app_competence', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_competence_name'), table_name='app_competence')
    op.drop_index(op.f('ix_app_competence_id'), table_name='app_competence')
    op.drop_table('app_competence')
    # ### end Alembic commands ###
