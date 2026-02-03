import sys
import os

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.teacher import Teacher
from app.models.world import World
from app.models.zone import Zone
from app.models.quest import Quest
from app.models.monster import Monster
from app.models.quiz_question import QuizQuestion

def seed_battle_data():
    db = SessionLocal()
    try:
        print("Seeding Battle Data...")

        # 1. Create a Teacher (if not exists)
        teacher = db.query(Teacher).filter(Teacher.email == "battle_master@guild.com").first()
        if not teacher:
            teacher = Teacher(
                username="BattleMaster",
                email="battle_master@guild.com",
                password_hash="hashed_secret"
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print(f"Created Teacher: {teacher.username}")
        else:
            print(f"Teacher exists: {teacher.username}")

        # 2. Create a World
        world = db.query(World).filter(World.title == "Battle Arena").first()
        if not world:
            world = World(
                title="Battle Arena",
                description="A place for combat.",
                teacher_id=teacher.teacher_id,
                is_published=True
            )
            db.add(world)
            db.commit()
            db.refresh(world)
            print(f"Created World: {world.title}")
        else:
             print(f"World exists: {world.title}")

        # 3. Create a Zone
        zone = db.query(Zone).filter(Zone.title == "Training Grounds", Zone.world_id == world.world_id).first()
        if not zone:
            zone = Zone(
                title="Training Grounds",
                description="Basic combat training.",
                world_id=world.world_id,
                order_index=1
            )
            db.add(zone)
            db.commit()
            db.refresh(zone)
            print(f"Created Zone: {zone.title}")

        # 4. Create a Quest
        quest = db.query(Quest).filter(Quest.title == "Defeat the Slime", Quest.zone_id == zone.zone_id).first()
        if not quest:
            quest = Quest(
                title="Defeat the Slime",
                description="A sticky situation.",
                zone_id=zone.zone_id,
                order_index=1,
                xp_reward=100,
                gold_reward=50
            )
            db.add(quest)
            db.commit()
            db.refresh(quest)
            print(f"Created Quest: {quest.title}")

        # 5. Create a Monster
        monster = db.query(Monster).filter(Monster.name == "Slime", Monster.quest_id == quest.quest_id).first()
        if not monster:
            monster = Monster(
                quest_id=quest.quest_id,
                name="Slime",
                description="A green gelatinous blob.",
                question_text="Defeated by answering questions!", 
                correct_answer="N/A", 
                wrong_options=[], 
                damage_per_wrong_answer=15,
                monster_hp=100,
                monster_image_url="https://placehold.co/200x200/green/white?text=Slime"
            )
            db.add(monster)
            db.commit()
            db.refresh(monster)
            print(f"Created Monster: {monster.name}")
        
        # 6. Create QuizQuestions
        questions = [
            {
                "text": "What is 2 + 2?",
                "correct": "4",
                "wrong": ["3", "5", "22"]
            },
            {
                "text": "Which language is this backend written in?",
                "correct": "Python",
                "wrong": ["Java", "C++", "Assembly"]
            },
            {
                "text": "What is the capital of France?",
                "correct": "Paris",
                "wrong": ["London", "Berlin", "Madrid"]
            },
            {
                "text": "What color is the sky (usually)?",
                "correct": "Blue",
                "wrong": ["Green", "Red", "Polka Dot"]
            },
             {
                "text": "Is P = NP?",
                "correct": "Unsolved",
                "wrong": ["Yes", "No", "Maybe"]
            }
        ]

        for q_data in questions:
            exists = db.query(QuizQuestion).filter(
                QuizQuestion.monster_id == monster.monster_id,
                QuizQuestion.question_text == q_data["text"]
            ).first()
            
            if not exists:
                q = QuizQuestion(
                    monster_id=monster.monster_id,
                    question_text=q_data["text"],
                    correct_answer=q_data["correct"],
                    wrong_answers=q_data["wrong"],
                    xp_value=10
                )
                db.add(q)
                print(f"Added question: {q_data['text']}")
        
        db.commit()
        print("Battle Data Seeded Successfully!")
        print(f"Monster ID for testing: {monster.monster_id}")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_battle_data()
