"""Add new worlds with icons for each class"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import World, Zone, Quest

def add_new_worlds():
    db = SessionLocal()
    try:
        # New worlds to add with icons
        new_worlds = [
            # 1 more for Warrior
            {
                "title": "Data Structures Arena",
                "description": "Master arrays, linked lists, trees, and graphs in the ultimate coding coliseum.",
                "difficulty": "Hard",
                "class": "Warrior",
                "icon": "⚔️",
                "zones": ["Arrays", "Linked Lists", "Trees", "Graphs", "Hash Tables", "Stacks & Queues"]
            },
            
            # 2 more for Mage
            {
                "title": "Machine Learning Sanctum",
                "description": "Harness the arcane power of neural networks and predictive algorithms.",
                "difficulty": "Expert",
                "class": "Mage",
                "icon": "🔮",
                "zones": ["Linear Regression", "Classification", "Neural Networks", "Deep Learning", "NLP", "Computer Vision"]
            },
            {
                "title": "Cloud Architecture Temple",
                "description": "Build and deploy scalable applications in the mystical cloud realms.",
                "difficulty": "Medium",
                "class": "Mage",
                "icon": "☁️",
                "zones": ["AWS Basics", "Docker", "Kubernetes", "Serverless", "CI/CD", "Microservices"]
            },
            
            # 2 more for Rogue
            {
                "title": "Cybersecurity Shadows",
                "description": "Learn the arts of ethical hacking and system defense in the dark web.",
                "difficulty": "Hard",
                "class": "Rogue",
                "icon": "🕵️",
                "zones": ["Network Security", "Web Exploits", "Cryptography", "Malware Analysis", "Forensics", "Social Engineering"]
            },
            {
                "title": "API Infiltration Base",
                "description": "Master REST, GraphQL, and WebSocket protocols to connect any system.",
                "difficulty": "Medium",
                "class": "Rogue",
                "icon": "🔌",
                "zones": ["REST Basics", "Authentication", "GraphQL", "WebSockets", "Rate Limiting", "API Design"]
            },
            
            # 2 more for Healer
            {
                "title": "Testing Monastery",
                "description": "Achieve enlightenment through the sacred practices of test-driven development.",
                "difficulty": "Medium",
                "class": "Healer",
                "icon": "🧪",
                "zones": ["Unit Testing", "Integration Tests", "E2E Testing", "TDD", "Mocking", "Code Coverage"]
            },
            {
                "title": "Documentation Gardens",
                "description": "Cultivate clear, beautiful documentation that heals confusing codebases.",
                "difficulty": "Easy",
                "class": "Healer",
                "icon": "📚",
                "zones": ["README Writing", "API Docs", "Code Comments", "Markdown", "Diagrams", "Tutorials"]
            },
        ]
        
        # Also update existing worlds with icons
        icon_map = {
            "C++ World": "⚙️",
            "JAVA World": "☕",
            "SQL World": "🗃️",
            "JavaScript World": "🌐",
            "AI World": "🤖",
            "The Python Caverns": "🐍",
            "The Git Graveyard": "👻",
            "The Debugging Ward": "🐛",
            "Refactoring Sanctuary": "♻️",
            "Penetration Peaks": "🔓",
            "Scripting Shadows": "📜",
            "Data Structures Arena": "⚔️",
        }
        
        # Update existing worlds with icons
        existing = db.query(World).all()
        for world in existing:
            if world.title in icon_map:
                world.icon = icon_map[world.title]
                print(f"Updated icon for {world.title}: {icon_map[world.title]}")
        
        # Create new worlds
        for w_data in new_worlds:
            # Check if exists
            exists = db.query(World).filter(World.title == w_data["title"]).first()
            if exists:
                print(f"World '{w_data['title']}' already exists, skipping...")
                continue
            
            print(f"\nCreating: {w_data['title']} ({w_data['class']})")
            
            world = World(
                teacher_id=7,  # MasterTeacher
                title=w_data["title"],
                description=w_data["description"],
                difficulty_level=w_data["difficulty"],
                is_published=True,
                required_class=w_data["class"],
                icon=w_data["icon"]
            )
            db.add(world)
            db.flush()
            
            # Create zones
            for z_idx, zone_title in enumerate(w_data["zones"]):
                zone = Zone(
                    world_id=world.world_id,
                    title=zone_title,
                    description=f"Master the concepts of {zone_title}.",
                    order_index=z_idx,
                    is_locked=(z_idx > 0),
                    unlock_requirement_xp=z_idx * 100
                )
                db.add(zone)
                db.flush()
                
                # Create 3 quests per zone
                for q_idx in range(3):
                    quest = Quest(
                        zone_id=zone.zone_id,
                        title=f"{zone_title}: Lesson {q_idx + 1}",
                        description=f"Complete lesson {q_idx + 1} of {zone_title}.",
                        xp_reward=50 + (q_idx * 25),
                        gold_reward=20 + (q_idx * 10),
                        order_index=q_idx
                    )
                    db.add(quest)
            
            print(f"  ✓ Created with {len(w_data['zones'])} zones")
        
        db.commit()
        print("\n✅ All new worlds created successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_new_worlds()
