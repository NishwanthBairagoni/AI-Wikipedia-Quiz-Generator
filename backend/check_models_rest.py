import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    data = response.json()
    
    with open("models_rest.txt", "w") as f:
        if "models" in data:
            for m in data["models"]:
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    f.write(f"{m['name']}\n")
        else:
             f.write(f"Error response: {data}\n")
except Exception as e:
    with open("models_rest.txt", "w") as f:
        f.write(f"Exception: {e}\n")
