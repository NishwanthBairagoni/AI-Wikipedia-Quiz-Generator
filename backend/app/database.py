from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the connection string (e.g., postgresql://user:password@localhost/dbname)
DATABASE_URL = os.getenv("DATABASE_URL")
# Safety check: Prevent the app from starting without a valid database connection
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")
# The Engine: The lowest level of SQLAlchemy that handles the actual connection to the DB
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Dependency: This function manages the lifecycle of a database session.
# It ensures a connection is opened when a request starts and closed when it finishes.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
