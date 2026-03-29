import os
from google import genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def draft_legal_text(facts: dict) -> str:
    from datetime import date
    current_date = date.today().strftime("%B %d, %Y")
    
    # Quick category classification to refine RAG search
    category_prompt = f"Classify this consumer complaint into one of these 5 categories: goods, service, airline, housing, medical. Complaint: {facts.get('core_issue')}. Return ONLY the category name."
    category_resp = client.models.generate_content(model='gemini-2.5-flash', contents=category_prompt)
    category = category_resp.text.strip().lower()

    from rag import retrieve_cases
    legal_precedents = retrieve_cases(facts.get('core_issue', ''), category=category)

    from jurisdiction import get_court_by_pincode
    forum_name = get_court_by_pincode(facts.get('user_pincode', ''))

    prompt = f"""Draft a formal Legal Notice under the Consumer Protection Act, 2019.

CRITICAL INSTRUCTIONS:
1. PERSPECTIVE: First-person ("I", "my") only.
2. CHRONOLOGY: Notice Date: {current_date}. Event Date: {facts.get('incident_date')}.
3. EVIDENCE TAGS: Based on "{facts.get('core_issue')}", insert 2-3 relevant placeholders:
   - Product complaint: [Invoice No. _____] [Serial/Model No. _____] [Warranty Card No. _____]
   - Refund dispute: [Order ID _____] [Refund Ticket No. _____]
   - Insurance: [Policy No. _____] [Claim Ref No. _____] [Rejection Letter date _____]
   - Service failure: [Booking/Contract No. _____] [Service Ticket No. _____]
   Use only the placeholders relevant to this case type.

4. STRUCTURE:
   - Header: BY REGISTERED AD / SPEED POST
   - Address Block: To, The Grievance Officer / Managing Director,
     {facts.get('opponent_name')}, {facts.get('opponent_address')}
   - Subject Line: RE: LEGAL NOTICE REGARDING {facts.get('core_issue').upper()} ON {facts.get('incident_date')}
   - Para 1: Purchase details, warranty/promise made. Establish sender as 
     "Consumer" under Section 2(7) of the Act.
   - Para 2: Specific defect/incident on {facts.get('incident_date')}.
   - Para 3: History of failed resolution attempts via customer care 
     (cite Ticket ID placeholder).
   - Para 4: Legal grounds. You must explicitly quote the statutory definitions of "Deficiency in Service" and/or "Unfair Trade Practice" from the provided Statutory Law. Then, cite the supporting Legal Precedents to prove why my specific case matches these legal definitions. \n{legal_precedents}
   - Para 5: Final Demand within 15 days:
     (a) {facts.get('desired_resolution')} of Rs. {facts.get('dispute_amount')}
     (b) Compensation of Rs. [10-25% of {facts.get('dispute_amount')}] 
         for mental agony and harassment
     (c) Litigation expenses of Rs. 5,000
     Failing which complaint will be filed before the {forum_name}.

5. TONE: Professional and firm. No emotional adjectives. Cite Section 2(7) 
   to establish consumer status in Para 1.

FACTS:
- Sender: {facts.get('user_name')}
- Sender City: {facts.get('user_city')} ({facts.get('user_pincode', 'No Pincode')})
- Opponent: {facts.get('opponent_name')}
- Opponent Address: {facts.get('opponent_address')}
- Amount: {facts.get('dispute_amount')}
- Core Issue: {facts.get('core_issue')}
- Desired Resolution: {facts.get('desired_resolution')}

CRITICAL RULE: Return ONLY the raw text of the notice. 
No Markdown. No preambles. No asterisks. No hashtags.
"""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text.strip()

import qrcode
from io import BytesIO
from reportlab.lib.utils import ImageReader

def generate_qr_image(session_id: str) -> ImageReader:
    """Generates a QR code image for the verification URL."""
    # This URL should lead to your frontend's verification route
    verify_url = f"https://nyaya-voice.vercel.app/verify/{session_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(verify_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL image to ReportLab compatible format
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return ImageReader(img_byte_arr)

def create_pdf(text: str, filepath: str, session_id: str = "123"):
    """Takes plain text and neatly formats it into a professional downloadable Indian court-style PDF with a QR verification code."""
    
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    # Create legal document-esque font styles (Times Roman)
    styles.add(ParagraphStyle(name='JustifiedText', alignment=TA_JUSTIFY, fontName="Times-Roman", fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='CenterHeading', alignment=TA_CENTER, fontName="Times-Bold", fontSize=14, spaceAfter=20, leading=18))
    
    flowables = []
    
    # 1. Add the QR Code to the top-right corner
    try:
        qr_img = generate_qr_image(session_id)
        # We'll use a spacer and then draw the QR code on the first page canvas if possible, 
        # but the simplest way is to add it as a flowable at the top.
        from reportlab.platypus import Image
        qr_flowable = Image(qr_img, width=60, height=60)
        qr_flowable.hAlign = 'RIGHT'
        flowables.append(qr_flowable)
        flowables.append(Spacer(1, -50)) # Pull the next text back up slightly
    except Exception as e:
        print(f"QR Generation Error: {e}")

    paragraphs = text.split('\n')
    for line in paragraphs:
        cleaned_line = line.strip()
        if not cleaned_line:
            flowables.append(Spacer(1, 10))
            continue
        
        # Format the top title bold and centered
        if "LEGAL NOTICE" in cleaned_line.upper() and len(cleaned_line) < 30:
            flowables.append(Paragraph(f"<b><u>{cleaned_line}</u></b>", styles["CenterHeading"]))
        else:
            # We must escape ampersands or brackets for ReportLab's XML parser just in case
            safe_text = cleaned_line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            flowables.append(Paragraph(safe_text, styles["JustifiedText"]))
            flowables.append(Spacer(1, 6))
            
    doc.build(flowables)
    return filepath
