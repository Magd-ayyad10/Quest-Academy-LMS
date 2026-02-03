from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.item import ItemRarity
import enum


class AchievementType(str, enum.Enum):
    """Enum for achievement types."""
    QUEST = "quest"
    COMBAT = "combat"
    SOCIAL = "social"
    COLLECTION = "collection"
    MASTERY = "mastery"


class Achievement(Base):
    """Achievement model - The Trophies."""
    
    __tablename__ = "achievements"
    
    achievement_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    achievement_type = Column(Enum(AchievementType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    icon_url = Column(Text)
    
    # Requirements
    requirement_value = Column(Integer, default=1)
    requirement_description = Column(Text)
    
    # Rewards
    xp_reward = Column(Integer, default=0)
    gold_reward = Column(Integer, default=0)
    title_reward = Column(String(100))
    
    # Rarity
    rarity = Column(Enum(ItemRarity, values_callable=lambda x: [e.value for e in x]), default=ItemRarity.COMMON)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Achievement {self.name}>"


class UserAchievement(Base):
    """UserAchievement model - The Trophy Case."""
    
    __tablename__ = "user_achievements"
    
    user_achievement_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.achievement_id", ondelete="CASCADE"), nullable=False, index=True)
    unlocked_at = Column(DateTime, server_default=func.now())
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
    
    def __repr__(self):
        return f"<UserAchievement User:{self.user_id} Achievement:{self.achievement_id}>"
