from sqlalchemy import create_engine, text
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)

with engine.connect() as conn:
    print(f"Connecting to: {settings.database_url}")
    try:
        # Try to select the new column
        result = conn.execute(text("SELECT required_class FROM assignments LIMIT 1"))
        print("Verification Success: 'required_class' column exists and is accessible.")
        for row in result:
            print(f"Sample data: {row}")
    except Exception as e:
        print(f"Verification FAILED: {e}")
