import sys
import os

sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models.world import World
from app.models.teacher import Teacher

def fix_ownership():
    db = SessionLocal()
    try:
        # Get our target teacher (ID 7)
        target_email = "teacher@questacademy.com"
        target_teacher = db.query(Teacher).filter(Teacher.email == target_email).first()
        
        if not target_teacher:
            print(f"Target teacher {target_email} not found!")
            return

        print(f"Target Teacher: {target_teacher.username} (ID: {target_teacher.teacher_id})")

        # Get all worlds
        worlds = db.query(World).all()
        print(f"Found {len(worlds)} worlds.")

        # Transfer ownership of specific seeded worlds or all? 
        # Let's transfer the newly seeded ones (C++, Java, etc) and maybe the Python ones.
        # Actually, let's just transfer ALL worlds to this teacher so the user sees everything.
        count = 0
        for world in worlds:
             # Only transfer if not already owned
             if world.teacher_id != target_teacher.teacher_id:
                 print(f"Transferring '{world.title}' from ID {world.teacher_id} to {target_teacher.teacher_id}...")
                 world.teacher_id = target_teacher.teacher_id
                 count += 1
        
        db.commit()
        print(f"Successfully transferred {count} worlds to {target_teacher.username}.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_ownership()
