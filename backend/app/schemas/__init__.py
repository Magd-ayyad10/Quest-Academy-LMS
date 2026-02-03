"""Pydantic Schemas Package"""
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserStats
from app.schemas.teacher import TeacherCreate, TeacherResponse, TeacherUpdate
from app.schemas.auth import Token, TokenData, LoginRequest
from app.schemas.world import WorldCreate, WorldResponse, WorldUpdate, WorldWithZones
from app.schemas.zone import ZoneCreate, ZoneResponse, ZoneUpdate, ZoneWithQuests
from app.schemas.quest import QuestCreate, QuestResponse, QuestUpdate, QuestWithDetails
from app.schemas.monster import MonsterCreate, MonsterResponse, MonsterUpdate, BattleRequest, BattleResult
from app.schemas.assignment import AssignmentCreate, AssignmentResponse, AssignmentUpdate
from app.schemas.submission import SubmissionCreate, SubmissionResponse, SubmissionGrade
from app.schemas.progress import ProgressResponse, ProgressUpdate
from app.schemas.item import ItemResponse, InventoryResponse, PurchaseRequest
from app.schemas.achievement import AchievementResponse, UserAchievementResponse
from app.schemas.leaderboard import LeaderboardEntryResponse
