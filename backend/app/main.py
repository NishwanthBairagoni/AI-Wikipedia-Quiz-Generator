from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import quiz



Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Wikipedia Quiz Generator")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(quiz.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Wikipedia Quiz Generator API"}
