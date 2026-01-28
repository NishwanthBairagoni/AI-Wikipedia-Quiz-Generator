from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import List
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    # Fallback/Mock if key is missing during dev initial setups, 
    # but in production we should raise. 
    # For now, let's assume the user will provide it.
    pass

# We redefine the Pydantic models here for the parser because it needs to be strictly nested
# effectively mirroring schema but used for parsing
class QuizQuestionLLM(BaseModel):
    question: str = Field(description="The question text")
    A: str = Field(description="Option A")
    B: str = Field(description="Option B")
    C: str = Field(description="Option C")
    D: str = Field(description="Option D")
    answer: str = Field(description="The correct option (A, B, C, or D)")
    difficulty: str = Field(description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(description="Short explanation grounded in the text")

class QuizOutputLLM(BaseModel):
    quiz: List[QuizQuestionLLM] = Field(description="List of 5-10 quiz questions")
    related_topics: List[str] = Field(description="List of 3-5 related Wikipedia topics")

def generate_quiz_from_text(text: str):
    if not GOOGLE_API_KEY:
         raise Exception("GOOGLE_API_KEY is not set.")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", google_api_key=GOOGLE_API_KEY, temperature=0.7)
    
    parser = PydanticOutputParser(pydantic_object=QuizOutputLLM)

    prompt = PromptTemplate(
        template="""You are an expert quiz generator. based on the following Wikipedia article content.
        
        Article Content:
        {text}

        Generate a quiz with the following requirements:
        1. Create 5 to 10 multiple-choice questions.
        2. Questions must be strictly grounded in the provided text.
        3. Do not hallucinate facts.
        4. Include a mix of difficulty levels (easy, medium, hard).
        5. Provide a short explanation for the correct answer.
        6. Suggest 3-5 related Wikipedia topics.
        
        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    models_to_try = [
        "gemini-1.5-flash-latest",
        "gemini-2.0-flash",
        "gemini-1.5-flash", 
        "gemini-1.5-flash-001",
        "gemini-1.5-pro",
        "gemini-1.0-pro", 
        "gemini-pro"
    ]

    errors = []
    
    for model_name in models_to_try:
        try:
            print(f"Attr: Trying model {model_name}...")
            # Re-initialize LLM with potential model
            # Force v1 API version
            llm = ChatGoogleGenerativeAI(
                model=model_name, 
                google_api_key=GOOGLE_API_KEY, 
                temperature=0.7,
                convert_system_message_to_human=True
            )
            chain = prompt | llm | parser
            result = chain.invoke({"text": text})
            return result
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            errors.append(f"{model_name}: {str(e)}")
            continue
            
    error_msg = "All models failed. Details: " + " | ".join(errors)
    print(error_msg)
    raise Exception(error_msg)
