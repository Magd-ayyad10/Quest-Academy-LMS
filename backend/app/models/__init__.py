"""SQLAlchemy Models Package"""
from app.models.user import User
from app.models.teacher import Teacher
from app.models.world import World
from app.models.zone import Zone
from app.models.quest import Quest
from app.models.monster import Monster
from app.models.quiz_question import QuizQuestion
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.models.progress import UserProgress
from app.models.item import Item, UserInventory
from app.models.achievement import Achievement, UserAchievement
from app.models.leaderboard import LeaderboardEntry
from app.models.engagement import (
    DailyQuest, UserDailyQuest, UserStreak, 
    UserActivity, WeeklyGoal, Friendship,
    DailyQuestType, ActivityType
)
from app.models.ai_grading import AIGradingLog
from app.models.notification import Notification

__all__ = [
    "User",
    "Teacher", 
    "World",
    "Zone",
    "Quest",
    "Monster",
    "Assignment",
    "Submission",
    "UserProgress",
    "Item",
    "UserInventory",
    "Achievement",
    "UserAchievement",
    "LeaderboardEntry",
    "DailyQuest",
    "UserDailyQuest",
    "UserStreak",
    "UserActivity",
    "WeeklyGoal",
    "Friendship",
    "AIGradingLog",
    "Notification",
]

