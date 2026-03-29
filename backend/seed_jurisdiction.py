import sqlite3
import os

def seed_jurisdiction_db():
    db_path = os.path.join(os.path.dirname(__file__), "jurisdiction.db")
    
    # Connect to (or create) the SQLite database
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pincode_mapping (
            pincode TEXT PRIMARY KEY,
            court_name TEXT NOT NULL,
            state TEXT NOT NULL
        )
    ''')
    
    # Seed with sample landmark data for the hackathon demo
    sample_data = [
        ('400001', 'District Consumer Disputes Redressal Commission, South Mumbai', 'Maharashtra'),
        ('400064', 'District Consumer Disputes Redressal Commission, North Mumbai', 'Maharashtra'),
        ('560001', 'Bangalore Urban District Consumer Disputes Redressal Commission', 'Karnataka'),
        ('110001', 'District Consumer Disputes Redressal Commission, New Delhi', 'Delhi'),
        ('600001', 'District Consumer Disputes Redressal Commission, Chennai', 'Tamil Nadu'),
        ('700001', 'District Consumer Disputes Redressal Commission, Kolkata Unit-I', 'West Bengal')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO pincode_mapping VALUES (?, ?, ?)', sample_data)
    
    conn.commit()
    conn.close()
    print(f"Jurisdiction Database seeded successfully at {db_path}")

if __name__ == "__main__":
    seed_jurisdiction_db()
