import os
import sys
from dotenv import load_dotenv

# Load environment variables FIRST
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from drafter import draft_legal_text, create_pdf

def test_drafting():
    print("Starting Test Drafting...")
    
    # Mock facts for a "goods" category case
    facts = {
        "user_name": "Anush",
        "user_city": "Mumbai",
        "user_pincode": "400001",
        "opponent_name": "Samsung India",
        "opponent_address": "Samsung Hub, Gurgaon, Haryana",
        "incident_date": "March 15, 2026",
        "dispute_amount": "50,000",
        "core_issue": "The brand new refrigerator stopped cooling within 2 days of purchase and the company is refusing a refund.",
        "desired_resolution": "Full Refund"
    }
    
    print(f"Generating legal notice text for: {facts['core_issue']}")
    notice_text = draft_legal_text(facts)
    
    print("-" * 30)
    print("GENERATED NOTICE PREVIEW:")
    print(notice_text[:500] + "...") # Print first 500 chars
    print("-" * 30)
    
    # Check for new headers
    if "BY REGISTERED AD / SPEED POST" in notice_text:
        print("SUCCESS: 'BY REGISTERED AD / SPEED POST' header found.")
    else:
        print("FAILURE: 'BY REGISTERED AD / SPEED POST' header NOT found.")
        
    if "SUBJECT LINE" in notice_text or "RE: LEGAL NOTICE" in notice_text:
        print("SUCCESS: Subject Line found.")
    else:
        print("FAILURE: Subject Line NOT found.")
        
    # Check for precedents (landmark cases)
    if "C.N. Anantharam V. Fiat India Ltd." in notice_text or "Precedent" in notice_text:
        print("SUCCESS: Legal precedents found in the text.")
    else:
        print("WARNING: No specific precedents found. Check RAG distance threshold or classification.")

    # Generate PDF
    pdf_path = "test_nyaya_notice.pdf"
    print(f"Generating PDF: {pdf_path}")
    create_pdf(notice_text, pdf_path)
    
    if os.path.exists(pdf_path):
        print(f"SUCCESS: PDF generated at {pdf_path}")
    else:
        print("FAILURE: PDF was not generated.")

if __name__ == "__main__":
    test_drafting()
