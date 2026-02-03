"""
Seed Daily Quests - Create default daily quests for the system
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings
from app.models.engagement import DailyQuest

settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_daily_quests():
    db = SessionLocal()
    
    try:
        # Check if quests already exist
        existing = db.query(DailyQuest).count()
        if existing > 0:
            print(f"Daily quests already exist ({existing}). Skipping...")
            return
        
        quests = [
            DailyQuest(
                title="Knowledge Seeker",
                description="Complete any lesson to earn bonus rewards",
                quest_type="complete_lesson",  # Use string value
                target_value=1,
                xp_reward=50,
                gold_reward=15,
                icon="📚"
            ),
            DailyQuest(
                title="Battle Ready",
                description="Win a quiz battle against a monster",
                quest_type="win_battle",
                target_value=1,
                xp_reward=75,
                gold_reward=25,
                icon="⚔️"
            ),
            DailyQuest(
                title="XP Hunter",
                description="Earn at least 100 XP today",
                quest_type="earn_xp",
                target_value=100,
                xp_reward=50,
                gold_reward=20,
                icon="⭐"
            ),
            DailyQuest(
                title="Gold Collector",
                description="Earn at least 50 gold today",
                quest_type="earn_gold",
                target_value=50,
                xp_reward=30,
                gold_reward=30,
                icon="🪙"
            ),
            DailyQuest(
                title="Daily Check-in",
                description="Log in to Quest Academy today",
                quest_type="login",
                target_value=1,
                xp_reward=25,
                gold_reward=10,
                icon="🎯"
            ),
            DailyQuest(
                title="Window Shopper",
                description="Visit the Merchant's Shop",
                quest_type="visit_shop",
                target_value=1,
                xp_reward=20,
                gold_reward=5,
                icon="🛒"
            ),
        ]
        
        for quest in quests:
            db.add(quest)
        
        db.commit()
        print(f"✅ Created {len(quests)} daily quests!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_daily_quests()
