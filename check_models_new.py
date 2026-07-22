import os
from google import genai

client = genai.Client(api_key="AIzaSyCbfTMRh_xUG8tUru-FuJv7r4La54lRQ0M")

try:
    print("Available Gemini Models for this Key:")
    for model in client.models.list():
        print(f"- {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
