import os
import json
from database import save_session, get_session
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    print("Testing Supabase Connection...")
    print(f"URL: {os.getenv('SUPABASE_URL')}")
    
    test_state = {
        "session_id": "test_123",
        "chat_history": [{"role": "user", "text": "Hello Supabase"}],
        "facts": {"user_name": "Test User"},
        "is_complete": False,
        "latest_response": "I see you!"
    }
    
    print("Saving test session...")
    save_session(test_state)
    
    print("Retrieving test session...")
    retrieved = get_session("test_123")
    
    if retrieved:
        print("SUCCESS! Data was saved and retrieved from Supabase.")
        print(f"Retrieved Facts: {retrieved['facts']}")
    else:
        print("FAILURE! Could not retrieve data. Check your Supabase table name and columns.")

if __name__ == "__main__":
    test_connection()
