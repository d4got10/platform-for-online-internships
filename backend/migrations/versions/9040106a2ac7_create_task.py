"""Create task

Revision ID: 9040106a2ac7
Revises: 0c180df3107f
Create Date: 2023-05-14 17:08:38.567303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9040106a2ac7'
down_revision = '0c180df3107f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_task',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('task_type', sa.Enum('single', 'multiple', 'text', 'excel', name='tasktype'), nullable=False),
    sa.Column('prev_task_id', sa.Integer(), nullable=True),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['prev_task_id'], ['app_task.id'], ),
    sa.ForeignKeyConstraint(['topic_id'], ['app_topic.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('topic_id', 'prev_task_id', name='u_prev_task_for_topic')
    )
    op.create_index(op.f('ix_app_task_id'), 'app_task', ['id'], unique=True)
    op.create_index(op.f('ix_app_task_name'), 'app_task', ['name'], unique=False)
    op.create_index(op.f('ix_app_task_prev_task_id'), 'app_task', ['prev_task_id'], unique=True)
    op.create_index(op.f('ix_app_task_task_type'), 'app_task', ['task_type'], unique=False)
    op.create_index(op.f('ix_app_task_topic_id'), 'app_task', ['topic_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_task_topic_id'), table_name='app_task')
    op.drop_index(op.f('ix_app_task_task_type'), table_name='app_task')
    op.drop_index(op.f('ix_app_task_prev_task_id'), table_name='app_task')
    op.drop_index(op.f('ix_app_task_name'), table_name='app_task')
    op.drop_index(op.f('ix_app_task_id'), table_name='app_task')
    op.drop_table('app_task')
    # ### end Alembic commands ###
    sa_enum = sa.Enum(name='tasktype')
    sa_enum.drop(op.get_bind(), checkfirst=True)
