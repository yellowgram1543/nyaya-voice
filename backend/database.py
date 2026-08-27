import os
import json
import sqlite3
from supabase import create_client, Client
from dotenv import load_dotenv

# Ensure env is loaded
load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

USE_SUPABASE = bool(URL and KEY)
supabase: Client = None

if USE_SUPABASE:
    try:
        supabase = create_client(URL, KEY)
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")
        USE_SUPABASE = False

SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "sessions.db")

def _init_sqlite():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            chat_history TEXT,
            facts TEXT,
            is_complete INTEGER,
            latest_response TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if not USE_SUPABASE:
    print("WARNING: Supabase credentials not found or failed. Using local SQLite fallback.")
    _init_sqlite()

def get_session(session_id: str) -> dict:
    """Retrieves the session state from Supabase or SQLite fallback."""
    if USE_SUPABASE:
        try:
            response = supabase.table("sessions").select("*").eq("session_id", session_id).execute()
            if response.data and len(response.data) > 0:
                row = response.data[0]
                return {
                    "session_id": session_id,
                    "chat_history": json.loads(row["chat_history"]) if row.get("chat_history") else [],
                    "facts": json.loads(row["facts"]) if row.get("facts") else {},
                    "is_complete": bool(row["is_complete"]),
                    "latest_response": row.get("latest_response", "")
                }
            return None
        except Exception as e:
            print(f"Supabase GET error: {e}")
            return None
    else:
        try:
            conn = sqlite3.connect(SQLITE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT chat_history, facts, is_complete, latest_response FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    "session_id": session_id,
                    "chat_history": json.loads(row[0]) if row[0] else [],
                    "facts": json.loads(row[1]) if row[1] else {},
                    "is_complete": bool(row[2]),
                    "latest_response": row[3] if row[3] else ""
                }
            return None
        except Exception as e:
            print(f"SQLite GET error: {e}")
            return None

def save_session(state: dict):
    """Saves or updates the session state in Supabase or SQLite fallback."""
    data = {
        "session_id": state["session_id"],
        "chat_history": json.dumps(state["chat_history"]),
        "facts": json.dumps(state["facts"]),
        "is_complete": state["is_complete"],
        "latest_response": state.get("latest_response", "")
    }
    
    if USE_SUPABASE:
        try:
            supabase.table("sessions").upsert(data).execute()
        except Exception as e:
            print(f"Supabase SAVE error: {e}")
    else:
        try:
            conn = sqlite3.connect(SQLITE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (session_id, chat_history, facts, is_complete, latest_response)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    chat_history=excluded.chat_history,
                    facts=excluded.facts,
                    is_complete=excluded.is_complete,
                    latest_response=excluded.latest_response,
                    updated_at=CURRENT_TIMESTAMP
            ''', (data["session_id"], data["chat_history"], data["facts"], int(data["is_complete"]), data["latest_response"]))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"SQLite SAVE error: {e}")

def update_session_facts(session_id: str, new_facts: dict):
    """Surgically updates only the facts dictionary for a session."""
    session = get_session(session_id)
    if not session:
        # Create it if it doesn't exist
        session = {
            "session_id": session_id,
            "chat_history": [],
            "facts": new_facts,
            "is_complete": False,
            "latest_response": ""
        }
    else:
        session["facts"].update(new_facts)
        
    save_session(session)
    print(f"Surgically updated facts for session {session_id}")

def get_all_completed_sessions():
    """Returns all completed legal notices from Supabase or SQLite."""
    if USE_SUPABASE:
        try:
            response = supabase.table("sessions").select("session_id, facts").eq("is_complete", True).execute()
            return [{"session_id": r["session_id"], "facts": json.loads(r["facts"]) if r.get("facts") else {}} for r in response.data]
        except Exception as e:
            print(f"Supabase B2B fetch error: {e}")
            return []
    else:
        try:
            conn = sqlite3.connect(SQLITE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT session_id, facts FROM sessions WHERE is_complete = 1")
            rows = cursor.fetchall()
            conn.close()
            return [{"session_id": row[0], "facts": json.loads(row[1]) if row[1] else {}} for row in rows]
        except Exception as e:
            print(f"SQLite B2B fetch error: {e}")
            return []
