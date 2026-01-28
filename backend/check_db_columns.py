import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def check_columns():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'quizzes';"
            ))
            columns = [row[0] for row in result]
            print(f"Columns in 'quizzes': {columns}")
            
            if 'key_entities' in columns:
                print("VERIFICATION SUCCESS: 'key_entities' found.")
            else:
                print("VERIFICATION FAILED: 'key_entities' NOT found.")
                
    except Exception as e:
        print(f"Error checking columns: {e}")

if __name__ == "__main__":
    check_columns()
