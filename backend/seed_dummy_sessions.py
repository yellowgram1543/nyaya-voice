import sqlite3
import json
import os
import uuid

DB_PATH = os.path.join(os.path.dirname(__file__), "nyaya_sessions.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Safely ensure the table exists just in case uvicorn hasn't spun up yet
cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    chat_history TEXT,
                    facts TEXT,
                    is_complete BOOLEAN,
                    latest_response TEXT
                  )''')

dummy_sessions = [
    {
        "session_id": str(uuid.uuid4())[:8],
        "chat_history": json.dumps([]),
        "facts": json.dumps({
            "user_name": "Meena Krishnan",
            "user_city": "Chennai",
            "user_pincode": "600001",
            "opponent_name": "Boat Lifestyle",
            "opponent_address": "Imagine Marketing Ltd, Mumbai",
            "incident_date": "March 1, 2025",
            "dispute_amount": "2999",
            "core_issue": "Bluetooth earphones stopped working after 10 days",
            "desired_resolution": "Replacement or full refund"
        }),
        "is_complete": True,
        "latest_response": "Ready to draft."
    },
    {
        "session_id": str(uuid.uuid4())[:8],
        "chat_history": json.dumps([]),
        "facts": json.dumps({
            "user_name": "Arjun Das",
            "user_city": "Kolkata",
            "user_pincode": "700001",
            "opponent_name": "Zomato Ltd",
            "opponent_address": "Ground Floor, Zomato Ltd, Gurgaon",
            "incident_date": "March 20, 2025",
            "dispute_amount": "350",
            "core_issue": "Food order delivered cold and incomplete",
            "desired_resolution": "Refund of Rs.350"
        }),
        "is_complete": True,
        "latest_response": "Ready to draft."
    },
    {
        "session_id": str(uuid.uuid4())[:8],
        "chat_history": json.dumps([]),
        "facts": json.dumps({
            "user_name": "Priya Nair",
            "user_city": "Mumbai",
            "user_pincode": "400050",
            "opponent_name": "Flipkart Internet Pvt Ltd",
            "opponent_address": "Vaishnavi Summit, Bengaluru 560034",
            "incident_date": "February 28, 2025",
            "dispute_amount": "4500",
            "core_issue": "Refund of Rs.4500 not processed for returned kurta after 45 days",
            "desired_resolution": "Immediate refund of Rs.4500"
        }),
        "is_complete": True,
        "latest_response": "Ready to draft."
    }
]

for s in dummy_sessions:
    cursor.execute('''INSERT OR REPLACE INTO sessions 
                      (session_id, chat_history, facts, is_complete, latest_response) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (s["session_id"], s["chat_history"], s["facts"], s["is_complete"], s["latest_response"]))

conn.commit()
conn.close()
print("Dummy sessions seeded successfully for the B2B Dashboard demo!")
