
import sys
import os
import random
from sqlalchemy.orm import Session

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal, engine, Base
from app.models import User, World, Zone, Quest, Monster, QuizQuestion

# Content Definitions
CONTENT_MAP = {
    "Mage": [
        {"topic": "Go", "title": "The Go Grove", "desc": "Mastering Golang concurrency and syntax."},
        {"topic": "Rust", "title": "The Rust Ridge", "desc": "Memory safety and systems programming."},
        {"topic": "Docker", "title": "The Docker Docks", "desc": "Containerization and microservices."},
        {"topic": "Kubernetes", "title": "The Kube Kingdom", "desc": "Orchestration at scale."},
        {"topic": "GraphQL", "title": "The Graph Galaxy", "desc": "Flexible API queries and mutations."},
        {"topic": "Cloud", "title": "The Cloud Citadel", "desc": "Advanced cloud infrastructure patterns."}
    ],
    "Ranger": [
        {"topic": "React", "title": "The React Realm", "desc": "Components, Hooks, and Virtual DOM."},
        {"topic": "TypeScript", "title": "The Type Tower", "desc": "Static typing for robust web apps."},
        {"topic": "Three.js", "title": "The Three Theater", "desc": "3D graphics in the browser."},
        {"topic": "Next.js", "title": "The Next Nexus", "desc": "Server-side rendering and static generation."},
        {"topic": "Flutter", "title": "The Flutter Fields", "desc": "Cross-platform mobile development."},
        {"topic": "State", "title": "The State Summit", "desc": "Complex state management architectures."}
    ],
    "Paladin": [
        {"topic": "Cybersecurity", "title": "The Cyber Castle", "desc": "Defense against digital threats."},
        {"topic": "CICD", "title": "The Pipeline Plains", "desc": "Continuous Integration and Deployment."},
        {"topic": "Linux", "title": "The Linux Labyrinth", "desc": "Kernel mastery and shell scripting."},
        {"topic": "Blockchain", "title": "The Chain Chamber", "desc": "Decentralized ledgers and smart contracts."},
        {"topic": "IaC", "title": "The Infra Isles", "desc": "Infrastructure as Code with Terraform."},
        {"topic": "Networking", "title": "The Net Necropolis", "desc": "Advanced networking protocols and security."}
    ]
}

def seed_content():
    db = SessionLocal()
    try:
        print("=== Seeding Advanced Content ===")
        
        for char_class, worlds_data in CONTENT_MAP.items():
            print(f"\nProcessing {char_class} Worlds...")
            
            # Fetch existing worlds for this class to update
            # We assume enforce_structure.py already guaranteed 6 worlds exist.
            existing_worlds = db.query(World).filter(World.required_class == char_class).order_by(World.world_id).all()
            
            # If fewer than 6, we might create (but enforce_structure should have handled it).
            # We'll just loop through min(existing, new_data)
            
            for i, world_data in enumerate(worlds_data):
                if i < len(existing_worlds):
                    world = existing_worlds[i]
                    print(f"  Updating World {world.world_id}: {world.title} -> {world_data['title']}")
                    
                    world.title = world_data['title']
                    world.description = world_data['desc']
                    world.icon = "🧙‍♂️" if char_class == "Mage" else "🏹" if char_class == "Ranger" else "🛡️"
                    world.difficulty_level = "Hard"
                    
                    # Ensure Zones
                    zones = db.query(Zone).filter(Zone.world_id == world.world_id).order_by(Zone.order_index).all()
                    
                    # We need 6 zones. enforce_structure ensured 6 zones exist.
                    # We will update them with thematic names
                    for z_idx, zone in enumerate(zones):
                        zone_topic = f"{world_data['topic']} Part {z_idx + 1}"
                        zone.title = f"{world_data['topic']} Zone {z_idx + 1}"
                        zone.description = f"Advanced studies in {world_data['topic']}."
                        
                        # Ensure Quests (3 Lessons + 1 Quiz)
                        quests = db.query(Quest).filter(Quest.zone_id == zone.zone_id).order_by(Quest.order_index).all()
                        
                        # Update/Create Lessons
                        # Structure: 3 Lessons (Index 0,1,2), 1 Quiz (Index 3)
                        
                        # LESSONS
                        for l_idx in range(3):
                            q_title = f"{world_data['topic']} Concept {z_idx+1}.{l_idx+1}"
                            if l_idx < len(quests):
                                # Update existing
                                q = quests[l_idx]
                                # Check if it's a monster quest (quiz), if so, we might have mapping issues if previous run was weird
                                # But we'll force it to be a lesson
                                q.title = q_title
                                q.content_url = "https://example.com/advanced_lesson"
                                q.xp_reward = 50
                                q.gold_reward = 10
                                # Ensure no monster
                                if q.monsters:
                                    for m in q.monsters:
                                        db.delete(m) # Clear old monsters from lessons
                            else:
                                # Create new
                                q = Quest(
                                    zone_id=zone.zone_id,
                                    title=q_title,
                                    content_url="https://example.com/advanced_lesson",
                                    xp_reward=50,
                                    gold_reward=10,
                                    order_index=l_idx
                                )
                                db.add(q)
                        
                        db.flush() # Sync
                        
                        # QUIZ (Index 3)
                        quiz_quest = None
                        if len(quests) > 3:
                            quiz_quest = quests[3]
                            quiz_quest.title = f"Boss: {world_data['topic']} Master"
                        else:
                             quiz_quest = Quest(
                                zone_id=zone.zone_id,
                                title=f"Boss: {world_data['topic']} Master",
                                xp_reward=50,
                                gold_reward=10,
                                order_index=3
                            )
                             db.add(quiz_quest)
                        
                        db.flush()
                        
                        # Ensure Monster
                        monster = db.query(Monster).filter(Monster.quest_id == quiz_quest.quest_id).first()
                        if not monster:
                            monster = Monster(
                                quest_id=quiz_quest.quest_id,
                                name=f"{world_data['topic']} Guardian",
                                description="A formidable foe.",
                                monster_hp=100,
                                damage_per_wrong_answer=15,
                                entry_cost=0,
                                pass_reward=50,
                                fail_penalty=10,
                                monster_image_url="/static/images/monsters/guardian.png",
                                question_text="What is the answer?", # Legacy
                                correct_answer="Correct", # Legacy
                                wrong_options=["Wrong"] # Legacy
                            )
                            db.add(monster)
                            db.flush()
                        else:
                            monster.name = f"{world_data['topic']} Guardian"
                        
                        # QUESTIONS (3 per Quiz)
                        existing_qs = db.query(QuizQuestion).filter(QuizQuestion.monster_id == monster.monster_id).all()
                        
                        needed_qs = 3 - len(existing_qs)
                        if needed_qs > 0:
                            for i in range(needed_qs):
                                qq = QuizQuestion(
                                    monster_id=monster.monster_id,
                                    question_text=f"Advanced Question {i+1} about {world_data['topic']}?",
                                    correct_answer="Correct Answer",
                                    wrong_answers=["Wrong 1", "Wrong 2", "Wrong 3"]
                                )
                                db.add(qq)
                                
            db.commit()
            print(f"✓ {char_class} updated.")

        print("\n=== Seeding Complete ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_content()
