import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

# Ensure env is loaded
load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase Client
supabase: Client = create_client(URL, KEY)

def get_session(session_id: str) -> dict:
    """Retrieves the session state from Supabase."""
    try:
        response = supabase.table("sessions").select("*").eq("session_id", session_id).execute()
        
        if response.data and len(response.data) > 0:
            row = response.data[0]
            return {
                "session_id": session_id,
                "chat_history": json.loads(row["chat_history"]),
                "facts": json.loads(row["facts"]),
                "is_complete": bool(row["is_complete"]),
                "latest_response": row["latest_response"]
            }
        return None
    except Exception as e:
        print(f"Supabase GET error: {e}")
        return None

def save_session(state: dict):
    """Saves or updates the session state in Supabase."""
    try:
        data = {
            "session_id": state["session_id"],
            "chat_history": json.dumps(state["chat_history"]),
            "facts": json.dumps(state["facts"]),
            "is_complete": state["is_complete"],
            "latest_response": state["latest_response"]
        }
        
        # 'upsert' in Supabase automatically handles 'INSERT OR REPLACE' logic
        supabase.table("sessions").upsert(data).execute()
        
    except Exception as e:
        print(f"Supabase SAVE error: {e}")

def update_session_facts(session_id: str, new_facts: dict):
    """Surgically updates only the facts dictionary for a session without touching other state."""
    try:
        # 1. Get current facts
        response = supabase.table("sessions").select("facts").eq("session_id", session_id).execute()
        
        current_facts = {}
        if response.data and len(response.data) > 0:
            current_facts = json.loads(response.data[0]["facts"])
        
        # 2. Merge
        current_facts.update(new_facts)
        
        # 3. Save back
        supabase.table("sessions").update({"facts": json.dumps(current_facts)}).eq("session_id", session_id).execute()
        print(f"Surgically updated facts for session {session_id}")
    except Exception as e:
        print(f"Supabase surgical update error: {e}")

# Note: You must manually create the 'sessions' table in your Supabase Dashboard:
# Table name: sessions
# Columns: session_id (text, PK), chat_history (text), facts (text), is_complete (bool), latest_response (text)

def get_all_completed_sessions():
    """Returns all completed legal notices for the B2B dashboard from Supabase."""
    try:
        response = supabase.table("sessions").select("session_id, facts").eq("is_complete", True).execute()
        return [{"session_id": r["session_id"], "facts": json.loads(r["facts"])} for r in response.data]
    except Exception as e:
        print(f"Supabase B2B fetch error: {e}")
        return []
