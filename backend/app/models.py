from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=False, index=True)
    title = Column(String)
    summary = Column(Text)
    sections = Column(JSON)
    quiz_data = Column(JSON) 
    related_topics = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
