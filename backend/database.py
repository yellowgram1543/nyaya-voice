import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "nyaya_sessions.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        chat_history TEXT,
                        facts TEXT,
                        is_complete BOOLEAN,
                        latest_response TEXT
                      )''')
    conn.commit()
    conn.close()

def get_session(session_id: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_history, facts, is_complete, latest_response FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "session_id": session_id,
            "chat_history": json.loads(row[0]),
            "facts": json.loads(row[1]),
            "is_complete": bool(row[2]),
            "latest_response": row[3]
        }
    return None

def save_session(state: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO sessions 
                      (session_id, chat_history, facts, is_complete, latest_response) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (state["session_id"], json.dumps(state["chat_history"]), 
                    json.dumps(state["facts"]), state["is_complete"], state["latest_response"]))
    conn.commit()
    conn.close()

def get_all_completed_sessions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, facts FROM sessions WHERE is_complete = 1")
    rows = cursor.fetchall()
    conn.close()
    return [{"session_id": r[0], "facts": json.loads(r[1])} for r in rows]

# Initialize upon import
init_db()
