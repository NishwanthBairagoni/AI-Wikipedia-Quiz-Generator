import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Quiz
from ..schemas import QuizRequest, QuizResponse
from ..services.scraper import scrape_wikipedia
from ..services.llm import generate_quiz_from_text

router = APIRouter(
    prefix="/api",
    tags=["quiz"]
)

def fix_quiz_format(quiz_data_list):
    """
    Helper to accept old flat format and convert to new nested format.
    Old: {question, A, B, C, D, ...}
    New: {question, options: {A, B, C, D}, ...}
    """
    fixed = []
    if not quiz_data_list:
        return []

    for q in quiz_data_list:
        if "options" in q:
            fixed.append(q)
        else:
            # Convert old format
            fixed.append({
                "question": q.get("question"),
                "options": {
                    "A": q.get("A"),
                    "B": q.get("B"),
                    "C": q.get("C"),
                    "D": q.get("D"),
                },
                "answer": q.get("answer"),
                "difficulty": q.get("difficulty"),
                "explanation": q.get("explanation")
            })
    return fixed

@router.post("/generate-quiz", response_model=QuizResponse)
def generate_quiz(request: QuizRequest, db: Session = Depends(get_db)):
    url_str = str(request.url)
    
    # Check if quiz already exists for this URL
    existing_quiz = db.query(Quiz).filter(Quiz.url == url_str).first()
    if existing_quiz:
        return {
            "id": existing_quiz.id,
            "url": existing_quiz.url,
            "title": existing_quiz.title,
            "summary": existing_quiz.summary,
            "sections": existing_quiz.sections,
            "quiz": fix_quiz_format(existing_quiz.quiz_data), 
            "related_topics": existing_quiz.related_topics,
            "created_at": existing_quiz.created_at
        }

    # Step 1: Scrape
    try:
        scraped_data = scrape_wikipedia(url_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Step 2: Generate Quiz (LLM)
    try:
        llm_output = generate_quiz_from_text(scraped_data["content_text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Generation Failed: {str(e)}")

    # Format quiz data for DB
    # We need to convert pydantic models to dicts for JSON storage
    
    formatted_quiz_data = []
    for q in llm_output.quiz:
        q_dict = q.dict()
        formatted_q = {
            "question": q_dict["question"],
            "options": {
                "A": q_dict["A"],
                "B": q_dict["B"],
                "C": q_dict["C"],
                "D": q_dict["D"],
            },
            "answer": q_dict["answer"],
            "difficulty": q_dict["difficulty"],
            "explanation": q_dict["explanation"]
        }
        formatted_quiz_data.append(formatted_q)
    
    # Step 3: Save to DB
    new_quiz = Quiz(
        url=url_str,
        title=scraped_data["title"],
        summary=scraped_data["summary"],
        sections=scraped_data["sections"],
        quiz_data=formatted_quiz_data,
        related_topics=llm_output.related_topics
    )
    
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    response_payload = {
        "id": new_quiz.id,
        "url": new_quiz.url,
        "title": new_quiz.title,
        "summary": new_quiz.summary,
        "sections": new_quiz.sections,
        "quiz": new_quiz.quiz_data, # Mapping quiz_data -> quiz
        "related_topics": new_quiz.related_topics,
        "created_at": new_quiz.created_at
    }

    # DEBUG: Save to file for user inspection
    try:
        with open("latest_quiz_output.json", "w", encoding="utf-8") as f:
            json.dump(response_payload, f, indent=2, default=str)
    except Exception as e:
        print(f"Failed to write debug json: {e}")

    return response_payload

@router.get("/history", response_model=List[QuizResponse])
def get_history(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).all()
    # We might need to map 'quiz_data' back to 'quiz' if the schema expects 'quiz'
    # But Pydantic's from_attributes should handle it if names match.
    # In model: quiz_data. In schema: quiz.
    # We rely on an implementation detail or map it manually.
    # Let's simple map it manually to be safe or update schema alias.
    # Schema 'quiz' field matches 'quiz' in response.
    # Model has 'quiz_data'.
    
    results = []
    for q in quizzes:
        # Create a dict from the model instance
        q_dict = {
            "id": q.id,
            "url": q.url,
            "title": q.title,
            "summary": q.summary,
            "sections": q.sections,
            "quiz": fix_quiz_format(q.quiz_data), # Mapping quiz_data -> quiz
            "related_topics": q.related_topics,
            "created_at": q.created_at
        }
        results.append(q_dict)
    return results

@router.get("/quiz/{quiz_id}", response_model=QuizResponse)
def get_quiz_detail(quiz_id: int, db: Session = Depends(get_db)):
    q = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {
        "id": q.id,
        "url": q.url,
        "title": q.title,
        "summary": q.summary,
        "sections": q.sections,
        "quiz": fix_quiz_format(q.quiz_data), 
        "related_topics": q.related_topics,
        "created_at": q.created_at
    }
