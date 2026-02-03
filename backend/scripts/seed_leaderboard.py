
import sys
import os
import random

# Add the parent directory to sys.path to resolve imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User
from app.services.auth_service import AuthService
from app.models.leaderboard import LeaderboardEntry

def seed_leaderboard():
    db = SessionLocal()
    
    # Fake users data
    fake_users = [
        {"username": "DragonSlayer99", "email": "dragon@test.com", "xp": 15400, "avatar_class": "Warrior", "level": 15},
        {"username": "CodeWizard", "email": "wizard@test.com", "xp": 14200, "avatar_class": "Mage", "level": 14},
        {"username": "ShadowRogue", "email": "rogue@test.com", "xp": 12800, "avatar_class": "Rogue", "level": 12},
        {"username": "HolyHealer", "email": "healer@test.com", "xp": 11500, "avatar_class": "Healer", "level": 11},
        {"username": "KnightOfPy", "email": "knight@test.com", "xp": 9800, "avatar_class": "Warrior", "level": 9},
        {"username": "JavaJester", "email": "jester@test.com", "xp": 8500, "avatar_class": "Rogue", "level": 8},
        {"username": "SQLSorcerer", "email": "sql@test.com", "xp": 7200, "avatar_class": "Mage", "level": 7},
        {"username": "GitPaladin", "email": "git@test.com", "xp": 6100, "avatar_class": "Paladin", "level": 6},
    ]

    print("🌱 Seeding leaderboard with heroes...")
    
    try:
        count = 0
        for data in fake_users:
            # Check if user exists
            user = db.query(User).filter(User.email == data["email"]).first()
            if not user:
                user = User(
                    username=data["username"],
                    email=data["email"],
                    password_hash=AuthService.get_password_hash("password123"),
                    current_xp=data["xp"],
                    level=data["level"],
                    # total_xp=data["xp"], # Removing as it's not in the model
                    gold=random.randint(100, 5000),
                    avatar_class=data["avatar_class"],
                    hp_current=100,
                    hp_max=100 + (data["level"] * 10)
                )
                db.add(user)
                db.flush() # Flush to get user_id
                count += 1
                print(f"Created hero: {user.username} (Lvl {user.level})")
            else:
                # Update existing dummy users to have high stats if they were already created
                user.current_xp = data["xp"]
                # existing.total_xp = data["xp"]
                user.level = data["level"]
                print(f"Updated hero: {user.username}")
            
            # Create or Update Leaderboard Entry
            lb_entry = db.query(LeaderboardEntry).filter(
                LeaderboardEntry.user_id == user.user_id,
                LeaderboardEntry.world_id == None # Global leaderboard
            ).first()
            
            if not lb_entry:
                lb_entry = LeaderboardEntry(
                    user_id=user.user_id,
                    total_xp=data["xp"],
                    rank_position=0, # Will be calculated dynamically or separate job
                    total_gold=user.gold
                )
                db.add(lb_entry)
            else:
                lb_entry.total_xp = data["xp"]
                lb_entry.total_gold = user.gold
        
        db.commit()
        print(f"✅ Successfully added/updated {count} heroes and their leaderboard entries!")
        
    except Exception as e:
        print(f"❌ Error seeding leaderboard: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_leaderboard()
