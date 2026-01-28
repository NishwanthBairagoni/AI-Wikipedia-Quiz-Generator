import os
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def log(msg):
    with open("migration_log.txt", "a") as f:
        f.write(msg + "\n")
    print(msg)

if not DATABASE_URL:
    log("Error: DATABASE_URL not found in .env")
    exit(1)

def migrate_db():
    log(f"Starting migration...")
    try:
        engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
        with engine.connect() as connection:
            log("Connected successfully.")
            
            
            log("Attempting to add 'key_entities' column...")
            try:
                connection.execute(text("ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS key_entities JSONB;"))
                log("SUCCESS: 'key_entities' column check/add completed.")
            except Exception as e:
                log(f"WARNING: Could not add 'key_entities': {e}")

            
            log("Attempting to add 'related_topics' column...")
            try:
                connection.execute(text("ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS related_topics JSONB;"))
                log("SUCCESS: 'related_topics' column check/add completed.")
            except Exception as e:
                log(f"WARNING: Could not add 'related_topics': {e}")
                
            log("Migration finished.")

    except Exception as e:
        log(f"CRITICAL ERROR during migration: {e}")

if __name__ == "__main__":
    
    with open("migration_log.txt", "w") as f:
        f.write("")
    migrate_db()
