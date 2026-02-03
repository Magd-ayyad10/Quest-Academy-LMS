"""
Engagement Models - Daily Quests, Streaks, Activity Tracking
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class DailyQuestType(str, enum.Enum):
    """Types of daily quests."""
    COMPLETE_LESSON = "complete_lesson"
    WIN_BATTLE = "win_battle"
    EARN_XP = "earn_xp"
    EARN_GOLD = "earn_gold"
    LOGIN = "login"
    VISIT_SHOP = "visit_shop"


class DailyQuest(Base):
    """Daily Quest template - The rotating daily challenges."""
    
    __tablename__ = "daily_quests"
    
    quest_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    quest_type = Column(String(50), nullable=False)  # Store as string
    target_value = Column(Integer, default=1)
    xp_reward = Column(Integer, default=50)
    gold_reward = Column(Integer, default=20)
    icon = Column(String(10), default="📋")
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user_progress = relationship("UserDailyQuest", back_populates="daily_quest", cascade="all, delete-orphan")


class UserDailyQuest(Base):
    """User's progress on daily quests."""
    
    __tablename__ = "user_daily_quests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    daily_quest_id = Column(Integer, ForeignKey("daily_quests.quest_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    current_progress = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    rewards_claimed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="daily_quests")
    daily_quest = relationship("DailyQuest", back_populates="user_progress")


class UserStreak(Base):
    """User's login/activity streak tracking."""
    
    __tablename__ = "user_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(Date)
    streak_start_date = Column(Date)
    
    # Relationships
    user = relationship("User", back_populates="streak")


class ActivityType(str, enum.Enum):
    """Types of activities to track."""
    QUEST_COMPLETE = "quest_complete"
    BATTLE_WON = "battle_won"
    BATTLE_LOST = "battle_lost"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    ITEM_PURCHASED = "item_purchased"
    LEVEL_UP = "level_up"
    WORLD_STARTED = "world_started"
    ZONE_COMPLETED = "zone_completed"


class UserActivity(Base):
    """Activity feed for users."""
    
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    activity_type = Column(String(50), nullable=False)  # Store as string
    title = Column(String(200), nullable=False)
    description = Column(Text)
    xp_earned = Column(Integer, default=0)
    gold_earned = Column(Integer, default=0)
    reference_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="activities")


class WeeklyGoal(Base):
    """Weekly goals for users."""
    
    __tablename__ = "weekly_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    week_start = Column(Date, nullable=False)
    xp_target = Column(Integer, default=500)
    xp_earned = Column(Integer, default=0)
    quests_target = Column(Integer, default=10)
    quests_completed = Column(Integer, default=0)
    battles_target = Column(Integer, default=3)
    battles_won = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="weekly_goals")


class Friendship(Base):
    """Friendship/Follow relationships between users."""
    
    __tablename__ = "friendships"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    friend_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), default="pending")  # pending, accepted, blocked
    created_at = Column(DateTime, server_default=func.now())
