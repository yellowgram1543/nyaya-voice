import sqlite3
import os

def get_court_by_pincode(pincode: str) -> str:
    """Takes a 6-digit Indian pincode and returns the District Commission name from our database.
    If not found, it returns a generic fallback name."""
    db_path = os.path.join(os.path.dirname(__file__), "jurisdiction.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # We query our SQLite 'memory'
        cursor.execute("SELECT court_name FROM pincode_mapping WHERE pincode = ?", (pincode,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]
        else:
            # Fallback logic for demo
            return f"the appropriate District Consumer Commission for the pincode area {pincode}"
            
    except Exception as e:
        print(f"Jurisdiction lookup error: {e}")
        return "the appropriate District Consumer Disputes Redressal Commission"

if __name__ == "__main__":
    # Test cases
    print(f"Test 400001: {get_court_by_pincode('400001')}")
    print(f"Test 560001: {get_court_by_pincode('560001')}")
    print(f"Test Unknown: {get_court_by_pincode('123456')}")
