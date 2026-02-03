from sqlalchemy import create_engine, text
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)

with engine.connect() as conn:
    print("Checking teachers...")
    result = conn.execute(text("SELECT teacher_id, user_id FROM teachers LIMIT 5"))
    teachers = list(result)
    print(f"Teachers found: {teachers}")
    
    if not teachers:
        print("No teachers found! Creating one linked to user 1...")
        # Try to find a user
        users = list(conn.execute(text("SELECT user_id FROM users LIMIT 1")))
        if users:
            uid = users[0][0]
            conn.execute(text(f"INSERT INTO teachers (user_id, bio) VALUES ({uid}, 'Guild Master')"))
            conn.commit()
            print(f"Created teacher for user {uid}")
            teacher_id = 1 # Assumption
        else:
            print("No users found. Cannot assign worlds.")
            exit()
    else:
        teacher_id = teachers[0][0]

    print(f"Assigning ALL worlds to Teacher ID {teacher_id}...")
    conn.execute(text(f"UPDATE worlds SET teacher_id = {teacher_id}"))
    conn.commit()
    print("Success. All worlds now belong to the primary teacher.")
