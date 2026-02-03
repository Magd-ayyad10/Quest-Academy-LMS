"""Add engagement tables

Revision ID: add_engagement_tables
Revises: 0c81906a8aa3
Create Date: 2026-01-26

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_engagement_tables'
down_revision = '0c81906a8aa3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Daily Quests table
    op.create_table(
        'daily_quests',
        sa.Column('quest_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('quest_type', sa.String(50), nullable=False),
        sa.Column('target_value', sa.Integer(), default=1),
        sa.Column('xp_reward', sa.Integer(), default=50),
        sa.Column('gold_reward', sa.Integer(), default=20),
        sa.Column('icon', sa.String(10), default='📋'),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.PrimaryKeyConstraint('quest_id')
    )
    op.create_index('ix_daily_quests_quest_id', 'daily_quests', ['quest_id'])

    # User Daily Quests table
    op.create_table(
        'user_daily_quests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('daily_quest_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('current_progress', sa.Integer(), default=0),
        sa.Column('is_completed', sa.Boolean(), default=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('rewards_claimed', sa.Boolean(), default=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['daily_quest_id'], ['daily_quests.quest_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_daily_quests_user_id', 'user_daily_quests', ['user_id'])

    # User Streaks table
    op.create_table(
        'user_streaks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('current_streak', sa.Integer(), default=0),
        sa.Column('longest_streak', sa.Integer(), default=0),
        sa.Column('last_activity_date', sa.Date(), nullable=True),
        sa.Column('streak_start_date', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_user_streaks_id', 'user_streaks', ['id'])

    # User Activities table
    op.create_table(
        'user_activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('activity_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('xp_earned', sa.Integer(), default=0),
        sa.Column('gold_earned', sa.Integer(), default=0),
        sa.Column('reference_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_activities_user_id', 'user_activities', ['user_id'])

    # Weekly Goals table
    op.create_table(
        'weekly_goals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('week_start', sa.Date(), nullable=False),
        sa.Column('xp_target', sa.Integer(), default=500),
        sa.Column('xp_earned', sa.Integer(), default=0),
        sa.Column('quests_target', sa.Integer(), default=10),
        sa.Column('quests_completed', sa.Integer(), default=0),
        sa.Column('battles_target', sa.Integer(), default=3),
        sa.Column('battles_won', sa.Integer(), default=0),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_weekly_goals_user_id', 'weekly_goals', ['user_id'])

    # Friendships table
    op.create_table(
        'friendships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('friend_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['friend_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_friendships_user_id', 'friendships', ['user_id'])
    op.create_index('ix_friendships_friend_id', 'friendships', ['friend_id'])


def downgrade() -> None:
    op.drop_table('friendships')
    op.drop_table('weekly_goals')
    op.drop_table('user_activities')
    op.drop_table('user_streaks')
    op.drop_table('user_daily_quests')
    op.drop_table('daily_quests')
