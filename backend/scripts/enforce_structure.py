
import sys
import os
import random
from sqlalchemy.orm import Session

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal, engine, Base
from app.models import User, World, Zone, Quest, Monster, QuizQuestion

# Classes
CLASSES = ["Warrior", "Mage", "Ranger", "Paladin"]
CLASS_MAP = {
    "Rogue": "Ranger",
    "Healer": "Paladin",
    "Warrior": "Warrior",
    "Mage": "Mage"
}

def enforce_structure():
    db = SessionLocal()
    try:
        print("=== Enforcing Structure for Classes: Warrior, Mage, Ranger, Paladin ===")
        
        # 1. Update existing mappings
        worlds = db.query(World).all()
        for w in worlds:
            if w.required_class in CLASS_MAP:
                if w.required_class != CLASS_MAP[w.required_class]:
                    print(f"Updating World '{w.title}' class from {w.required_class} to {CLASS_MAP[w.required_class]}")
                    w.required_class = CLASS_MAP[w.required_class]
            elif w.required_class not in CLASSES and w.required_class != 'All':
                 # Assign random class or keep as is? Let's assign to Mage by default if unknown
                 pass
        db.commit()

        # 2. Ensure each class has 6 Worlds
        teacher_id = 1 # Default Admin
        
        for char_class in CLASSES:
            class_worlds = db.query(World).filter(World.required_class == char_class).all()
            count = len(class_worlds)
            print(f"Class {char_class} has {count} worlds.")
            
            if count < 6:
                needed = 6 - count
                print(f"Creating {needed} new worlds for {char_class}...")
                for i in range(needed):
                    new_world = World(
                        teacher_id=teacher_id,
                        title=f"{char_class} Advanced Training {i+1}",
                        description=f"Advanced concepts for {char_class}s.",
                        difficulty_level="Medium",
                        required_class=char_class,
                        is_published=True,
                        icon="🏰"
                    )
                    db.add(new_world)
                db.commit()
            
            # Re-fetch worlds
            class_worlds = db.query(World).filter(World.required_class == char_class).all()
            
            # 3. Ensure 6 Zones per World
            for world in class_worlds:
                zones = db.query(Zone).filter(Zone.world_id == world.world_id).all()
                z_count = len(zones)
                
                if z_count < 6:
                    z_needed = 6 - z_count
                    if z_needed > 0:
                        print(f"  World '{world.title}' has {z_count} zones. Creating {z_needed} more...")
                        for i in range(z_needed):
                            new_zone = Zone(
                                world_id=world.world_id,
                                title=f"Zone {z_count + i + 1} - {world.title}",
                                description="A dangerous area.",
                                order_index=z_count + i
                            )
                            db.add(new_zone)
                        db.commit()
                
                # Re-fetch zones
                zones = db.query(Zone).filter(Zone.world_id == world.world_id).all()
                
                # 4. Ensure 3 Lessons + 1 Quiz per Zone
                for zone in zones:
                    quests = db.query(Quest).filter(Quest.zone_id == zone.zone_id).order_by(Quest.order_index).all()
                    
                    # Separate lessons and quizzes ( монsters)
                    lessons = [q for q in quests if not q.monsters]
                    quizzes = [q for q in quests if q.monsters] # or len(q.monsters) > 0
                    
                    # Fix: Query monsters separately if relationship not loaded? 
                    # Actually ORM should handle it, but let's be safe.
                    # We will create new ones if needed.
                    
                    # We want exactly 4 quests: 3 lessons, 1 quiz.
                    # Index 0, 1, 2 = Lessons. Index 3 = Quiz.
                    
                    l_count = len(lessons)
                    q_count = len(quizzes)
                    
                    current_total = len(quests)
                    
                    # Add Lessons
                    if l_count < 3:
                        l_needed = 3 - l_count
                        for i in range(l_needed):
                            new_lesson = Quest(
                                zone_id=zone.zone_id,
                                title=f"Lesson {l_count + i + 1}: Theory",
                                content_url="https://example.com/lesson",
                                xp_reward=50,
                                gold_reward=10,
                                order_index=l_count + i
                            )
                            db.add(new_lesson)
                            lessons.append(new_lesson)
                    
                    # Add Quiz
                    if q_count < 1:
                        quiz_entry = Quest(
                            zone_id=zone.zone_id,
                            title=f"Boss Battle: {zone.title}",
                            content_url="", # Quiz
                            xp_reward=50,
                            gold_reward=10,
                            order_index=3
                        )
                        db.add(quiz_entry)
                        db.flush() # get ID
                        
                        # Add Monster
                        monster = Monster(
                            quest_id=quiz_entry.quest_id,
                            name="Zone Guardian",
                            description="Defender of the zone.",
                            monster_hp=100,
                            damage_per_wrong_answer=10,
                            entry_cost=0,
                            pass_reward=50,
                            fail_penalty=10,
                            monster_image_url="/static/images/monsters/guardian.png",
                            # Legacy required fields
                            question_text="Legacy Question",
                            correct_answer="Legacy Answer",
                            wrong_options=["Option 1", "Option 2"]
                        )
                        db.add(monster)
                        db.flush()
                        
                        # Add Sample Question
                        qq = QuizQuestion(
                            monster_id=monster.monster_id,
                            question_text="What is the answer to life?",
                            correct_answer="42",
                            wrong_answers=["0", "100", "NaN"]
                        )
                        db.add(qq)
                        quizzes.append(quiz_entry)
                    
                    db.commit()
                    
                    # Force 50 XP / 10 Gold on all quests in this structure
                    # Reload quests to include newly added
                    all_zone_quests = db.query(Quest).filter(Quest.zone_id == zone.zone_id).all()
                    for q in all_zone_quests:
                        if q.xp_reward != 50 or q.gold_reward != 10:
                            q.xp_reward = 50
                            q.gold_reward = 10
                    db.commit()

        print("=== Structure Enforcement Complete ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    enforce_structure()
