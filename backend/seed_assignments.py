"""Seed sample assignments for testing"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Assignment, Quest, Zone, World

def seed_assignments():
    db = SessionLocal()
    try:
        # Get some quests to attach assignments to
        quests = db.query(Quest).limit(10).all()
        
        if not quests:
            print("No quests found! Run seed_worlds_v2.py first.")
            return
        
        print(f"Found {len(quests)} quests. Creating sample assignments...")
        
        assignments_data = [
            {"title": "Hello World Challenge", "description": "Write your first program in this language.", "xp": 50, "gold": 25, "max_score": 100},
            {"title": "Variables Workshop", "description": "Practice declaring and using variables.", "xp": 75, "gold": 40, "max_score": 100},
            {"title": "Logic Gate Master", "description": "Complete the logic puzzle to prove your understanding.", "xp": 100, "gold": 60, "max_score": 100},
            {"title": "Loop Labyrinth", "description": "Navigate the loops and find the exit.", "xp": 150, "gold": 80, "max_score": 100},
            {"title": "Function Fortress", "description": "Build reusable functions to solve complex problems.", "xp": 200, "gold": 100, "max_score": 100},
        ]
        
        created = 0
        for i, quest in enumerate(quests[:5]):
            # Check if assignment already exists for this quest
            existing = db.query(Assignment).filter(Assignment.quest_id == quest.quest_id).first()
            if existing:
                print(f"  Skipping quest {quest.quest_id} - already has assignments")
                continue
            
            data = assignments_data[i % len(assignments_data)]
            
            assignment = Assignment(
                quest_id=quest.quest_id,
                title=f"{data['title']} - {quest.title}",
                description=data['description'],
                max_score=data['max_score'],
                xp_reward=data['xp'],
                gold_reward=data['gold'],
                due_date=datetime.now() + timedelta(days=7 + i)  # Due in 7-12 days
            )
            db.add(assignment)
            created += 1
            print(f"  ✓ Created: {assignment.title}")
        
        db.commit()
        print(f"\n✅ Created {created} sample assignments!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_assignments()
