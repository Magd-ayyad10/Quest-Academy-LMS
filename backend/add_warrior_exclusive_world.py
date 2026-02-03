
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import World, Zone, Quest, Teacher

def add_warrior_world():
    db = SessionLocal()
    try:
        # Get a teacher (MasterTeacher)
        teacher = db.query(Teacher).filter(Teacher.username == "MasterTeacher").first()
        if not teacher:
            # Fallback to first teacher or create one if needed, but let's assume one exists from seeds
            teacher = db.query(Teacher).first()
            
        if not teacher:
            print("No teacher found to assign the world to.")
            return

        # World Data
        world_data = {
            "title": "Algorithms Coliseum",
            "description": "Prove your might in the arena of logic! Only the strongest Warriors can master these complex algorithms.",
            "difficulty": "Hard",
            "class": "Warrior",
            "icon": "🏛️",
            "zones": ["Sorting Arena", "Searching Grounds", "Dynamic Programming Dungeon", "Greedy Gauntlet", "Backtracking Bastion"]
        }

        # Check if exists
        exists = db.query(World).filter(World.title == world_data["title"]).first()
        if exists:
            print(f"World '{world_data['title']}' already exists.")
            return

        print(f"Creating World: {world_data['title']} (Class: {world_data['class']})")
        
        world = World(
            teacher_id=teacher.teacher_id,
            title=world_data["title"],
            description=world_data["description"],
            difficulty_level=world_data["difficulty"],
            is_published=True,
            required_class=world_data["class"],
            icon=world_data["icon"]
        )
        db.add(world)
        db.flush()
        
        # Create zones
        for z_idx, zone_title in enumerate(world_data["zones"]):
            zone = Zone(
                world_id=world.world_id,
                title=zone_title,
                description=f"Conquer the {zone_title}.",
                order_index=z_idx,
                is_locked=(z_idx > 0), # Lock all except first
                unlock_requirement_xp=z_idx * 150
            )
            db.add(zone)
            db.flush()
            
            # Create quests
            for q_idx in range(4): # 4 quests per zone
                quest = Quest(
                    zone_id=zone.zone_id,
                    title=f"{zone_title} Challenge {q_idx + 1}",
                    # description removed
                    xp_reward=100 + (q_idx * 50),
                    gold_reward=50 + (q_idx * 20),
                    order_index=q_idx
                )
                db.add(quest)
        
        db.commit()
        print(f"Successfully created '{world_data['title']}' for Warriors only.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_warrior_world()
