from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Notification(Base):
    """Notification model - Alerts for users."""
    
    __tablename__ = "notifications"
    
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Notification content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    icon = Column(String(10), default="📢")  # Emoji icon
    notification_type = Column(String(50), default="general")  # assignment, achievement, system, etc.
    
    # Related entity (optional)
    related_id = Column(Integer, nullable=True)  # e.g., assignment_id
    related_type = Column(String(50), nullable=True)  # e.g., "assignment"
    
    # Status
    is_read = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.notification_id}: {self.title}>"
