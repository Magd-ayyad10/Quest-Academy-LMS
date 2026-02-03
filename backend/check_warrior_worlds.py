from app.database import SessionLocal
from app.models.world import World
from app.models.teacher import Teacher

def check_warrior_worlds():
    db = SessionLocal()
    try:
        # Get Warrior worlds
        warrior_worlds = db.query(World).filter(World.required_class == "Warrior").all()
        
        print(f"=== Warrior Worlds ===")
        for w in warrior_worlds:
            teacher = db.query(Teacher).filter(Teacher.teacher_id == w.teacher_id).first()
            teacher_name = teacher.username if teacher else "NO TEACHER"
            print(f"World ID: {w.world_id}, Title: {w.title}, Teacher ID: {w.teacher_id}, Teacher: {teacher_name}")
        
        print(f"\n=== All Worlds ===")
        all_worlds = db.query(World).all()
        for w in all_worlds:
            teacher = db.query(Teacher).filter(Teacher.teacher_id == w.teacher_id).first()
            teacher_name = teacher.username if teacher else "NO TEACHER"
            print(f"World ID: {w.world_id}, Title: {w.title}, Class: {w.required_class}, Teacher ID: {w.teacher_id}, Teacher: {teacher_name}")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_warrior_worlds()
