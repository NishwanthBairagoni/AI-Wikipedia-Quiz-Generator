import os
import google.generativeai as genai
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv()
# Retrieve the API key and configure the Generative AI library
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# A list of specific model strings to probe for availability 
models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
    "gemini-1.0-pro",
    "gemini-1.0-pro-001",
    "gemini-pro"
]

# Open a text file to log the results of the availability test
with open("probe_results.txt", "w") as f:
    # Log a masked version of the API key for security/verification
    f.write(f"Testing API Key: {api_key[:5]}...***\n")
    for model in models_to_test:
        f.write(f"Testing {model} ... ")
        try:
            # Attempt to initialize the model and send a simple prompt
            m = genai.GenerativeModel(model)
            response = m.generate_content("Hello")
            # Check if the model returned a valid text response
            if response and response.text:
                f.write("SUCCESS\n")
            else:
                f.write("Failed (No output)\n")
        except Exception as e:
            f.write(f"FAILED: {e}\n")
