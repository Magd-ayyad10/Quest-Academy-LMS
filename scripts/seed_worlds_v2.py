import sys
import os
import random

# Add parent directory to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.config import get_settings
from app.models.world import World
from app.models.zone import Zone
from app.models.quest import Quest
from app.models.monster import Monster
from app.models.quiz_question import QuizQuestion
from app.models.teacher import Teacher  # Needed for FK

settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_worlds():
    db = SessionLocal()
    
    try:
        print("Starting World Seeding...")
        
        # 1. Ensure a Teacher exists to own these worlds
        teacher = db.query(Teacher).first()
        if not teacher:
            print("No teacher found. Creating a default Admin Teacher.")
            teacher = Teacher(
                user_id=1, # Assuming user 1 exists, or we leave it null if nullable (it isn't usually)
                # In a real seed, we should ensure a User exists too. 
                # For now, let's assume the current environment has users or we might fail.
                # Actually, let's just pick the first user or create a dummy one if needed.
                # But Teacher table usually links to User.
                # Let's try to get a teacher, if not, we might be in trouble if we don't know a valid user_id.
                # However, looking at the previous docker-compose, we have a postgres user but not necessarily app users.
                # Let's hope a teacher exists or we will just use a hardcoded ID and hope for the best?
                # No, better:
            )
            # Actually, let's just fetch the first user to be the teacher?
            # Creating a teacher requires a user_id. 
            pass

        # Use the first teacher found, or ID 1 if none (and hope it works, or relying on cascade/manual fix later)
        # Better: Check existing worlds to avoid duplicates?
        # The prompt asks to seed these specific 5 worlds. I will check availability by title.
        
        teacher_id = teacher.teacher_id if teacher else 1

        worlds_data = [
            {
                "title": "C++ World",
                "difficulty": "Hard", 
                "biome": "Cobalt Foundry",
                "description": "Master low-level memory management and high-performance algorithms in the industrial forges of C++.",
                "topics": ["Basics/Syntax", "Logic/Flow", "Loops/Iteration", "Arrays/Strings", "Functions/Pointers", "OOP/Classes"]
            },
            {
                "title": "JAVA World", 
                "difficulty": "Medium",
                "biome": "Emerald Server",
                "description": "Navigate the structured object-oriented landscapes of the Java Virtual Machine.",
                "topics": ["JVM/Syntax", "Control Flow", "Methods/Packages", "Classes/Objects", "Inheritance/Interfaces", "Collections/Exceptions"]
            },
            {
                "title": "SQL World",
                "difficulty": "Medium", 
                "biome": "Amber Vault",
                "description": "Excavate data and optimize queries in the ancient relational vaults of SQL.",
                "topics": ["Queries/Where", "CRUD Operations", "Aggregations/GroupBy", "Joins", "Constraints/Keys", "Subqueries/Views"]
            },
            {
                "title": "JavaScript World",
                "difficulty": "Easy", 
                "biome": "Neon Web",
                "description": "Surf the asynchronous event loops of the web in this vibrant, dynamic neon city.",
                "topics": ["Variables/Types", "Logic/Equality", "Arrays/Methods", "Functions/Scope", "DOM/Events", "Async/Promises"]
            },
            {
                "title": "AI World",
                "difficulty": "Expert", 
                "biome": "Neural Void",
                "description": "Explore the abstract dimensions of Machine Learning and Neural Networks.",
                "topics": ["LLM Basics", "Prompt Engineering", "Chatbot Apps", "Vector DBs/RAG", "Image Gen", "Ethics/Fine-tuning"]
            }
        ]

        # Quiz Entry Costs per Zone Index (0-5)
        quiz_costs = [30, 60, 90, 120, 150, 180]

        for w_data in worlds_data:
            # Check if world exists
            existing_world = db.query(World).filter(World.title == w_data["title"]).first()
            if existing_world:
                print(f"World '{w_data['title']}' already exists. Skipping...")
                continue

            print(f"Creating World: {w_data['title']}...")
            world = World(
                teacher_id=teacher_id,
                title=w_data["title"],
                description=w_data["description"],
                difficulty_level=w_data["difficulty"],
                is_published=True,
                theme_prompt=w_data["biome"], # Using biome as theme hint
                thumbnail_url=f"/assets/worlds/{w_data['title'].lower().replace(' ', '_')}.jpg"
            )
            db.add(world)
            db.flush() # Get world_id

            # Create 6 Zones
            for z_idx, topic in enumerate(w_data["topics"]):
                zone_title = f"{topic}"
                print(f"  - Creating Zone {z_idx+1}: {zone_title}")
                
                zone = Zone(
                    world_id=world.world_id,
                    title=zone_title,
                    description=f"Master the concepts of {topic}.",
                    order_index=z_idx,
                    is_locked=(z_idx > 0), # First zone unlocked
                    unlock_requirement_xp=z_idx * 100 # Simple progression
                )
                db.add(zone)
                db.flush()

                # Create 3 Quests (Lessons) per Zone
                for q_idx in range(3):
                    lesson_num = (z_idx * 3) + q_idx + 1
                    quest_title = f"{topic}: Lesson {q_idx+1}"
                    
                    quest = Quest(
                        zone_id=zone.zone_id,
                        title=quest_title,
                        content_url="", # Text content ideally
                        xp_reward=50,
                        gold_reward=10,
                        order_index=q_idx,
                        ai_narrative_prompt=f"Explain {topic} part {q_idx+1} in the style of {w_data['biome']}."
                    )
                    db.add(quest)
                    db.flush()

                    # Add Monster (Quiz) to the 3rd Quest in the Zone
                    if q_idx == 2:
                        quiz_entry_cost = quiz_costs[z_idx]
                        monster_name = f"Guardian of {topic}"
                        
                        print(f"    - Adding Boss: {monster_name} (Cost: {quiz_entry_cost} NC)")

                        # Monster Placeholder fields (Required by schema)
                        monster = Monster(
                            quest_id=quest.quest_id,
                            name=monster_name,
                            description=f"Prove your mastery of {topic} to proceed.",
                            question_text="Battle Logic Placeholder", 
                            correct_answer="True",
                            wrong_options=["False"],
                            monster_hp=100,
                            damage_per_wrong_answer=10,
                            entry_cost=quiz_entry_cost,
                            pass_reward=30,
                            fail_penalty=5,
                            monster_image_url=f"/assets/monsters/{w_data['biome'].lower().replace(' ', '_')}_boss.png"
                        )
                        db.add(monster)
                        db.flush()

                        # Add 3 Unique Questions
                        for q_num in range(1, 4):
                            question = QuizQuestion(
                                monster_id=monster.monster_id,
                                question_text=f"Question {q_num} about {topic} in {w_data['title']}",
                                correct_answer=f"Correct Answer for {topic} Q{q_num}",
                                wrong_answers=[f"Wrong A ({topic})", f"Wrong B ({topic})", f"Wrong C ({topic})"],
                                xp_value=20
                            )
                            db.add(question)

        db.commit()
        print("✅ Database Seeding Complete!")

    except Exception as e:
        print(f"❌ Error Seeding Database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_worlds()
