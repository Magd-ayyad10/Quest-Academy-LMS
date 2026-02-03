from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class LeaderboardEntry(Base):
    """LeaderboardEntry model - The Hall of Fame."""
    
    __tablename__ = "leaderboard_entries"
    
    entry_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    world_id = Column(Integer, ForeignKey("worlds.world_id", ondelete="CASCADE"), index=True)
    
    # Scores
    total_xp = Column(Integer, default=0, nullable=False)
    total_gold = Column(Integer, default=0, nullable=False)
    quests_completed = Column(Integer, default=0, nullable=False)
    monsters_defeated = Column(Integer, default=0, nullable=False)
    achievements_unlocked = Column(Integer, default=0, nullable=False)
    
    # Ranking
    rank_position = Column(Integer)
    
    # Time period
    period_start = Column(Date)
    period_end = Column(Date)
    
    # Metadata
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="leaderboard_entries")
    world = relationship("World", back_populates="leaderboard_entries")
    
    def __repr__(self):
        return f"<LeaderboardEntry User:{self.user_id} Rank:{self.rank_position}>"
