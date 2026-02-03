import sys
import os
import requests
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import AuthService
from app.models.monster import Monster

client = TestClient(app)

def get_test_token(db: Session):
    # Ensure test user exists
    email = "hero@test.com"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            username="TestHero",
            password_hash=AuthService.get_password_hash("password123"),
            level=1,
            hp_current=100,
            hp_max=100,
            current_xp=0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create token
    # Login to get token
    response = client.post("/api/auth/login", data={"username": email, "password": "password123"})
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return None
    return response.json()["access_token"]

def test_battle_flow():
    db = SessionLocal()
    try:
        # 1. Get Token
        token = get_test_token(db)
        if not token:
            print("Could not get auth token. Aborting.")
            return

        headers = {"Authorization": f"Bearer {token}"}
        print("Authenticated successfully.")

        # 2. Find the Slime Monster
        monster = db.query(Monster).filter(Monster.name == "Slime").first()
        if not monster:
            print("Monster 'Slime' not found. Run seed script first.")
            return

        monster_id = monster.monster_id
        print(f"Testing against Monster ID: {monster_id}")

        # 3. Get Battle State
        res = client.get(f"/api/battle/{monster_id}", headers=headers)
        if res.status_code != 200:
            print(f"Failed to get battle state: {res.text}")
            return
        
        state = res.json()
        print(f"Battle State loaded. HP: {state['player_hp']}, Monster HP %: {state['monster_hp_pct']}")
        questions = state['questions']
        if not questions:
            print("No questions found!")
            return
        
        first_q = questions[0]
        q_id = first_q['question_id']
        print(f"First Question: {first_q['question_text']}")
        
        # We need to know the correct answer to test properly.
        # Ideally we shouldn't know it from API, but for testing we can query DB.
        from app.models.quiz_question import QuizQuestion
        db_q = db.query(QuizQuestion).filter(QuizQuestion.question_id == q_id).first()
        correct_answer = db_q.correct_answer
        
        print(f"Correct Answer (from DB): {correct_answer}")

        # 4. Attack with Correct Answer
        print("Attacking with CORRECT answer...")
        payload = {
            "question_id": q_id,
            "answer": correct_answer
        }
        res = client.post("/api/battle/attack", json=payload, headers=headers)
        if res.status_code != 200:
            print(f"Attack failed: {res.text}")
        else:
            data = res.json()
            print(f"Result: {data['message']}")
            print(f"Damage Dealt: {data['damage_dealt']}")
            print(f"Is Correct: {data['is_correct']}")
            if not data['is_correct']:
                print("ERROR: Answer should have been correct!")

        # 5. Attack with Wrong Answer
        print("Attacking with WRONG answer...")
        payload = {
            "question_id": q_id,
            "answer": "This is definitely wrong"
        }
        res = client.post("/api/battle/attack", json=payload, headers=headers)
        if res.status_code != 200:
            print(f"Attack failed: {res.text}")
        else:
            data = res.json()
            print(f"Result: {data['message']}")
            print(f"Damage Received: {data['damage_received']}")
            print(f"Is Correct: {data['is_correct']}")
            if data['is_correct']:
                print("ERROR: Answer should have been wrong!")

        print("Test Complete.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_battle_flow()
