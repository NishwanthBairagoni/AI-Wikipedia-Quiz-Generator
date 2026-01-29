from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import quiz


# Automatically create database tables based on SQLAlchemy models 
# defined in 'Base' when the application starts.
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application instance
app = FastAPI(title="AI Wikipedia Quiz Generator")

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the quiz router to organize endpoints under separate modules
app.include_router(quiz.router)

# Basic health check or landing endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to AI Wikipedia Quiz Generator API"}
