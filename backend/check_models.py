import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv


sys.stdout.reconfigure(line_buffering=True)

print("Starting checks...", flush=True)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

print(f"Checking models for key: {api_key[:5]}...", flush=True)

try:
    for m in genai.list_models():
        print(f"Found model: {m.name}")
        if 'generateContent' in m.supported_generation_methods:
            print(f" - SUPPORTED: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
