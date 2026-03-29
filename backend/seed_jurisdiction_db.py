import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "jurisdiction.db")

def seed():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pincode_mapping (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pincode TEXT UNIQUE,
                        court_name TEXT
                      )''')
    
    data = [
        ("400001", "District Consumer Disputes Redressal Commission, South Mumbai, Maharashtra"),
        ("400050", "Suburban District Consumer Disputes Redressal Commission, Bandra, Mumbai"),
        ("110001", "District Consumer Disputes Redressal Forum (Central), Maharana Pratap ISBT, New Delhi"),
        ("560001", "Bangalore Urban District Consumer Disputes Redressal Commission, Karnataka"),
        ("560055", "Bangalore Urban II (North) Consumer Disputes Redressal Commission, Karnataka"),
        ("600001", "District Consumer Disputes Redressal Forum (North Chennai), Tamil Nadu"),
        ("700001", "Kolkata Unit-I District Consumer Disputes Redressal Commission, West Bengal"),
        ("411001", "Pune District Consumer Disputes Redressal Forum, Maharashtra"),
        ("500001", "Hyderabad District Consumer Disputes Redressal Forum, Telangana")
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO pincode_mapping (pincode, court_name) VALUES (?, ?)", data)
    conn.commit()
    conn.close()
    print("jurisdiction.db seeded successfully!")

if __name__ == "__main__":
    seed()
