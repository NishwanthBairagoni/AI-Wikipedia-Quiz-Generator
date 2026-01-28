# AI Wikipedia Quiz Generator

A full-stack application that generates interactive quizzes from Wikipedia articles using Google Gemini LLM.

## Tech Stack

- **Backend**: Python (FastAPI), SQLAlchemy, PostgreSQL, LangChain, BeautifulSoup
- **Frontend**: React (Vite), Tailwind CSS, Axios, Lucide React

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL Database
- Google Gemini API Key

## Setup & Installation

### 1. Database Setup
Ensure your PostgreSQL server is running. Create a database named `wikipedia_quiz` (or whatever you prefer).

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Configuration**:
Rename `.env.example` to `.env` and update the values:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/wikipedia_quiz
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Run Server**:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Docs at `http://localhost:8000/docs`.

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
The UI will be available at `http://localhost:5173`.

## Usage

1. Open the Frontend.
2. In the "Generate Quiz" tab, paste a Wikipedia URL (e.g., `https://en.wikipedia.org/wiki/Python_(programming_language)`).
3. Click "Generate Quiz".
4. Take the quiz!
5. Check "Past Quizzes" to see your history.

## Project Structure

```
/backend
  /app
    /routers    # API Endpoints
    /services   # Logic (Scraper, LLM)
    main.py     # Entry point
    models.py   # DB Models
    schemas.py  # Pydantic Schemas
    database.py # DB Config

/frontend
  /src
    /components
      QuizGenerator.jsx  # Input Form
      QuizView.jsx       # Interactive Quiz
      History.jsx        # Past Quizzes
    App.jsx
    api.js
```
