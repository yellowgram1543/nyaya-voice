import os
from google import genai

client = genai.Client(api_key="AIzaSyDc95594I2vp6JamxY1dPYT4AdSEAWz_QY")

try:
    print("Available Gemini Models for this Key:")
    for model in client.models.list():
        print(f"- {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
