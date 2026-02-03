from app.database import SessionLocal
from app.models.teacher import Teacher

def list_teachers():
    db = SessionLocal()
    try:
        teachers = db.query(Teacher).all()
        print(f"Total Teachers: {len(teachers)}")
        for t in teachers:
            print(f"Teacher ID: {t.teacher_id}, Username: {t.username}, Email: {t.email}")
    finally:
        db.close()

if __name__ == "__main__":
    list_teachers()
