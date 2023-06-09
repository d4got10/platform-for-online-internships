"""Create Subdivision and Post

Revision ID: dd8cab8d69f5
Revises: ab35b63119c0
Create Date: 2023-05-23 00:46:19.066351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd8cab8d69f5'
down_revision = 'ab35b63119c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_subdivision',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.Text(), server_default='', nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_subdivision_id'), 'app_subdivision', ['id'], unique=True)
    op.create_index(op.f('ix_app_subdivision_name'), 'app_subdivision', ['name'], unique=True)
    op.create_table('app_post',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.Text(), server_default='', nullable=False),
    sa.Column('subdivision_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['subdivision_id'], ['app_subdivision.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_post_id'), 'app_post', ['id'], unique=True)
    op.create_index(op.f('ix_app_post_name'), 'app_post', ['name'], unique=True)
    op.create_index(op.f('ix_app_post_subdivision_id'), 'app_post', ['subdivision_id'], unique=False)
    op.create_table('app_user_post_association',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('post_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['app_post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_index(op.f('ix_app_user_post_association_post_id'), 'app_user_post_association', ['post_id'], unique=False)
    op.create_index(op.f('ix_app_user_post_association_user_id'), 'app_user_post_association', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_user_post_association_user_id'), table_name='app_user_post_association')
    op.drop_index(op.f('ix_app_user_post_association_post_id'), table_name='app_user_post_association')
    op.drop_table('app_user_post_association')
    op.drop_index(op.f('ix_app_post_subdivision_id'), table_name='app_post')
    op.drop_index(op.f('ix_app_post_name'), table_name='app_post')
    op.drop_index(op.f('ix_app_post_id'), table_name='app_post')
    op.drop_table('app_post')
    op.drop_index(op.f('ix_app_subdivision_name'), table_name='app_subdivision')
    op.drop_index(op.f('ix_app_subdivision_id'), table_name='app_subdivision')
    op.drop_table('app_subdivision')
    # ### end Alembic commands ###
