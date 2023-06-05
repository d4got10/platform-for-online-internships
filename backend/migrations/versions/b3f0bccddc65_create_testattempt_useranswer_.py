"""Create TestAttempt, UserAnswer, UserCompetence

Revision ID: b3f0bccddc65
Revises: a28bb6191a7d
Create Date: 2023-06-06 01:47:47.076648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3f0bccddc65'
down_revision = 'a28bb6191a7d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_usercompetence',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('competence_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competence_id'], ['app_competence.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_usercompetence_competence_id'), 'app_usercompetence', ['competence_id'], unique=False)
    op.create_index(op.f('ix_app_usercompetence_id'), 'app_usercompetence', ['id'], unique=True)
    op.create_index(op.f('ix_app_usercompetence_user_id'), 'app_usercompetence', ['user_id'], unique=False)
    op.create_table('app_testattempt',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_to_pass', sa.Integer(), nullable=False),
    sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['topic_id'], ['app_topic.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_testattempt_id'), 'app_testattempt', ['id'], unique=True)
    op.create_index(op.f('ix_app_testattempt_topic_id'), 'app_testattempt', ['topic_id'], unique=False)
    op.create_index(op.f('ix_app_testattempt_user_id'), 'app_testattempt', ['user_id'], unique=False)
    op.create_table('app_useranswer',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=True),
    sa.Column('text_answer', sa.Text(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.CheckConstraint('NOT (answer_id IS NULL AND text_answer IS NULL)', name='check_answer_is_set'),
    sa.ForeignKeyConstraint(['answer_id'], ['app_answer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_useranswer_id'), 'app_useranswer', ['id'], unique=True)
    op.create_index(op.f('ix_app_useranswer_user_id'), 'app_useranswer', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_useranswer_user_id'), table_name='app_useranswer')
    op.drop_index(op.f('ix_app_useranswer_id'), table_name='app_useranswer')
    op.drop_table('app_useranswer')
    op.drop_index(op.f('ix_app_testattempt_user_id'), table_name='app_testattempt')
    op.drop_index(op.f('ix_app_testattempt_topic_id'), table_name='app_testattempt')
    op.drop_index(op.f('ix_app_testattempt_id'), table_name='app_testattempt')
    op.drop_table('app_testattempt')
    op.drop_index(op.f('ix_app_usercompetence_user_id'), table_name='app_usercompetence')
    op.drop_index(op.f('ix_app_usercompetence_id'), table_name='app_usercompetence')
    op.drop_index(op.f('ix_app_usercompetence_competence_id'), table_name='app_usercompetence')
    op.drop_table('app_usercompetence')
    # ### end Alembic commands ###
