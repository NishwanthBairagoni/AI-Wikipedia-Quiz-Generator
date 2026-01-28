import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

with open("available_models.txt", "w") as f:
    try:
        f.write("Checking models...\n")
        files = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
                files.append(m.name)
        
        if not files:
            f.write("No models found with generateContent capability.\n")
            
    except Exception as e:
        f.write(f"Error: {e}\n")
