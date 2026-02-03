from sqlalchemy import create_engine, text
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)

with engine.connect() as conn:
    print("Migrating Database...")
    try:
        conn.execute(text("ALTER TABLE assignments ADD COLUMN required_class VARCHAR(50) DEFAULT 'All'"))
        conn.commit()
        print("Successfully added 'required_class' column to 'assignments' table.")
    except Exception as e:
        print(f"Migration failed (Column might already exist): {e}")
