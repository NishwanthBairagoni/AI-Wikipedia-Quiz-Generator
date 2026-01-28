import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


log_file = os.path.join(os.path.dirname(__file__), "force_migration.log")

def log(msg):
    print(msg)
    with open(log_file, "a") as f:
        f.write(msg + "\n")

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def force_migration():
    if not DATABASE_URL:
        log("ERROR: DATABASE_URL is missing.")
        return

    log(f"Connecting to: {DATABASE_URL}")
    try:
        
        engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
        with engine.connect() as connection:
            log("Connection successful.")
            
            
            log("Executing: ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS key_entities JSONB")
            try:
                connection.execute(text("ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS key_entities JSONB;"))
                log("SUCCESS: key_entities column added (or already exists).")
            except Exception as e:
                log(f"ERROR adding key_entities: {e}")

            
            log("Executing: ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS related_topics JSONB")
            try:
                connection.execute(text("ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS related_topics JSONB;"))
                log("SUCCESS: related_topics column added (or already exists).")
            except Exception as e:
                log(f"ERROR adding related_topics: {e}")
                
            log("Migration sequence finished.")
            
    except Exception as e:
        log(f"CRITICAL DB CONNECTION ERROR: {e}")

if __name__ == "__main__":
   
    with open(log_file, "w") as f:
        f.write("Starting Migration...\n")
    force_migration()
