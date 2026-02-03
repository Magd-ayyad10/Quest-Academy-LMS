
import sys
import os
from datetime import date

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, DailyQuest, UserDailyQuest, UserStreak, UserActivity, WeeklyGoal
from app.routers.engagement import get_or_create_streak, get_or_create_weekly_goal

def test_dashboard_queries():
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if not user:
            print("❌ No users found!")
            return

        print(f"Testing for user: {user.username} (ID: {user.user_id})")

        # 1. Daily Quests
        print("Testing Daily Quests...")
        dqs = db.query(DailyQuest).all()
        print(f"✅ Daily Quests found: {len(dqs)}")

        # 2. Streak
        print("Testing Streak...")
        try:
            streak = get_or_create_streak(db, user.user_id)
            print(f"✅ Streak: {streak.current_streak}")
        except Exception as e:
            print(f"❌ Streak failed: {e}")

        # 3. Weekly Goals
        print("Testing Weekly Goals...")
        try:
            weekly = get_or_create_weekly_goal(db, user.user_id)
            print(f"✅ Weekly Goal XP: {weekly.xp_earned}")
        except Exception as e:
            print(f"❌ Weekly Goals failed: {e}")

        # 4. Skills
        print("Testing Skills...")
        try:
            from app.models import World, Quest, Zone, UserProgress
            worlds = db.query(World).filter(World.is_published == True).all()
            print(f"✅ Worlds found: {len(worlds)}")
            for w in worlds:
                 q_count = db.query(Quest).join(Zone).filter(Zone.world_id == w.world_id).count()
                 print(f"   - World {w.title}: {q_count} quests")
        except Exception as e:
             print(f"❌ Skills failed: {e}")

        # 5. Continue Journey
        print("Testing Continue Journey...")
        try:
             last = db.query(UserProgress).filter(UserProgress.user_id == user.user_id).first()
             print(f"✅ User Progress entries found: {last is not None}")
        except Exception as e:
             print(f"❌ Continue Journey failed: {e}")

    except Exception as e:
        print(f"❌ General Database Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_dashboard_queries()
