
import sys
import os
from sqlalchemy import text

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import World

def seed_class_worlds():
    db = SessionLocal()
    print("🌱 Seeding Class-Exclusive Worlds...")

    new_worlds = [
        # HEALER WORLDS (Maintenance/Repair)
        {
            "title": "The Debugging Ward", 
            "description": "Learn the art of diagnosing and curing code ailments. Master breakpoints and stack traces to heal broken applications.",
            "difficulty": "Medium",
            "class": "Healer",
            "thumb": "🏥"
        },
        {
            "title": "Refactoring Sanctuary", 
            "description": "Cleanse dirty code and restore order. Improve structure without changing behavior to keep the codebase healthy.",
            "difficulty": "Hard",
            "class": "Healer",
            "thumb": "✨"
        },
        {
            "title": "Testing Temple", 
            "description": "Erect barriers against bugs using Unit Tests and Integration Tests. Prevention is the best medicine.",
            "difficulty": "Medium",
            "class": "Healer",
            "thumb": "🛡️"
        },

        # MAGE WORLDS (Complexity/AI)
        {
            "title": "Algorithm Arcana", 
            "description": "Weave complex spells of logic. Master sorting, searching, and dynamic programming to bend data to your will.",
            "difficulty": "Hard",
            "class": "Mage",
            "thumb": "🔮"
        },
        {
            "title": "Neural Nexus", 
            "description": "Tap into the hive mind. Build artificial intelligence models that learn and evolve on their own.",
            "difficulty": "Expert",
            "class": "Mage",
            "thumb": "🧠"
        },
        {
            "title": "Data Sorcery", 
            "description": "Conjure insights from raw chaos. Use Pandas and NumPy to visualize and manipulate vast datasets.",
            "difficulty": "Medium",
            "class": "Mage",
            "thumb": "📊"
        },

        # ROGUE WORLDS (Security/Automation)
        {
            "title": "Penetration Peaks", 
            "description": "Learn to pick the locks of digital fortresses. Ethical hacking and vulnerability scanning.",
            "difficulty": "Hard",
            "class": "Rogue",
            "thumb": "🕵️"
        },
        {
            "title": "Scripting Shadows", 
            "description": "Move unseen and automate the mundane. Shell scripting and automation for the silent operator.",
            "difficulty": "Medium",
            "class": "Rogue",
            "thumb": "📜"
        },
        {
            "title": "Cryptography Crypt", 
            "description": "Speak in riddles and codes. Encrypt messages and break ciphers to secure communications.",
            "difficulty": "Hard",
            "class": "Rogue",
            "thumb": "🔐"
        }
    ]

    for w_data in new_worlds:
        exists = db.query(World).filter(World.title == w_data["title"]).first()
        if not exists:
            world = World(
                title=w_data["title"],
                description=w_data["description"],
                difficulty_level=w_data["difficulty"],
                thumbnail_url=w_data["thumb"],
                is_published=True,
                required_class=w_data["class"],  # Enforcing Class Exclusivity
                teacher_id=1
            )
            db.add(world)
            print(f"Created World: {w_data['title']} ({w_data['class']} Only)")
        else:
            # Update existing to be class specific if re-run
            exists.required_class = w_data["class"]
            exists.difficulty_level = w_data["difficulty"]
            print(f"Updated World: {w_data['title']}")

    db.commit()
    db.close()
    print("✅ Done! 9 Class-Exclusive worlds added.")

if __name__ == "__main__":
    seed_class_worlds()
