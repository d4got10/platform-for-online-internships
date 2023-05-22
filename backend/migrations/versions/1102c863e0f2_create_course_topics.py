"""Create course topics

Revision ID: 1102c863e0f2
Revises: 34ef22eb976d
Create Date: 2023-05-14 14:34:02.407774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1102c863e0f2'
down_revision = '34ef22eb976d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_topic',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('prev_topic_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['app_course.id'], ),
    sa.ForeignKeyConstraint(['prev_topic_id'], ['app_topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_topic_course_id'), 'app_topic', ['course_id'], unique=False)
    op.create_index(op.f('ix_app_topic_id'), 'app_topic', ['id'], unique=True)
    op.create_index(op.f('ix_app_topic_name'), 'app_topic', ['name'], unique=False)
    op.create_index(op.f('ix_app_topic_prev_topic_id'), 'app_topic', ['prev_topic_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_topic_prev_topic_id'), table_name='app_topic')
    op.drop_index(op.f('ix_app_topic_name'), table_name='app_topic')
    op.drop_index(op.f('ix_app_topic_id'), table_name='app_topic')
    op.drop_index(op.f('ix_app_topic_course_id'), table_name='app_topic')
    op.drop_table('app_topic')
    # ### end Alembic commands ###