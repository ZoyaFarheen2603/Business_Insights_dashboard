import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-3.5-flash")

response = model.generate_content(
    "Explain what Power BI is in one sentence."
)

print(response.text)