from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Any
from datetime import datetime

class QuizRequest(BaseModel):
    url: HttpUrl

class QuestionOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

class QuizQuestion(BaseModel):
    question: str
    options: QuestionOption
    answer: str
    difficulty: str
    explanation: str

class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]
    created_at: datetime

    class Config:
        from_attributes = True
