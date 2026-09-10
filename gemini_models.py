import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("\nModels supporting generateContent\n")
print("-" * 100)

for model in client.models.list():
    methods = getattr(model, "supported_actions", None)

    if methods is None:
        methods = getattr(model, "supportedGenerationMethods", [])

    if methods:
        if any("generateContent" in str(m) for m in methods):
            print(model.name)
            print("Supported Methods:", methods)
            print()

print("-" * 100)