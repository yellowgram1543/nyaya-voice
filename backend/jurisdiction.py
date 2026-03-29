import sqlite3
import os
import requests

def get_court_by_pincode(pincode: str) -> str:
    """Takes a 6-digit Indian pincode and returns the District Commission name.
    Checks local DB first, then dynamically queries the Indian Postal API for 19,000+ codes."""
    db_path = os.path.join(os.path.dirname(__file__), "jurisdiction.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Local Database Override (for specific zone routing like South Mumbai)
        cursor.execute("SELECT court_name FROM pincode_mapping WHERE pincode = ?", (pincode,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
            
        # 2. Dynamic API Mapping (For the remaining 19,000+ Pincodes across India!)
        try:
            resp = requests.get(f"https://api.postalpincode.in/pincode/{pincode}", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data and isinstance(data, list) and data[0].get("Status") == "Success":
                    post_office = data[0]["PostOffice"][0]
                    district = post_office.get("District", "")
                    state = post_office.get("State", "")
                    if district:
                        return f"District Consumer Disputes Redressal Commission, {district}, {state}"
        except Exception as api_err:
            print(f"Postal API fetch failed: {api_err}")
            
        # 3. Absolute Fallback if API is down or pincode is invalid
        return f"the appropriate District Consumer Commission for the pincode area {pincode}"
            
    except Exception as e:
        print(f"Jurisdiction lookup error: {e}")
        return "the appropriate District Consumer Disputes Redressal Commission"

if __name__ == "__main__":
    # Test cases
    print(f"Test 400001 (Mumbai Local DB): {get_court_by_pincode('400001')}")
    print(f"Test 122018 (Gurugram Dynamic API): {get_court_by_pincode('122018')}")
    print(f"Test 734001 (Darjeeling Dynamic API): {get_court_by_pincode('734001')}")
