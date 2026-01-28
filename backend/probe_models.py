import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
    "gemini-1.0-pro",
    "gemini-1.0-pro-001",
    "gemini-pro"
]

with open("probe_results.txt", "w") as f:
    f.write(f"Testing API Key: {api_key[:5]}...***\n")
    for model in models_to_test:
        f.write(f"Testing {model} ... ")
        try:
            m = genai.GenerativeModel(model)
            response = m.generate_content("Hello")
            if response and response.text:
                f.write("SUCCESS\n")
            else:
                f.write("Failed (No output)\n")
        except Exception as e:
            f.write(f"FAILED: {e}\n")
