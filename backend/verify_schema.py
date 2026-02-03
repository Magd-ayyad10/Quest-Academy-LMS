from sqlalchemy import create_engine, inspect
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)
inspector = inspect(engine)

table_name = "ai_grading_logs"
if inspector.has_table(table_name):
    print(f"Table '{table_name}' exists.")
    columns = inspector.get_columns(table_name)
    for col in columns:
        print(f"Column: {col['name']} - {col['type']}")
else:
    print(f"Table '{table_name}' does NOT exist.")
