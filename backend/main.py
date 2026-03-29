from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

app = FastAPI(
    title="Nyaya-Voice API",
    description="Backend for the AI-Driven Pro-Bono Legal Intake Agent",
    version="1.0.0"
)

# Enable CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # During dev, allow all. In prod, restrict to React app URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Request Model
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    status: str

# SQLite database for persistent state tracking across server restarts
from database import get_session, save_session, get_all_completed_sessions

@app.get("/")
async def root():
    return {"message": "Nyaya-Voice API is running. The Nervous System is online."}

@app.get("/api/b2b/notices")
async def get_all_notices():
    """Returns all completed legal notices for the B2B dashboard."""
    return get_all_completed_sessions()

@app.get("/api/verify/{session_id}")
async def verify_notice(session_id: str):
    """Verifies the authenticity of a legal notice via QR Code."""
    session_data = get_session(session_id)
    if not session_data or not session_data.get("is_complete"):
        raise HTTPException(status_code=404, detail="Authentic Notice Not Found")
    return {"status": "Verified", "session_id": session_id, "facts": session_data["facts"]}

@app.get("/api/b2b/risk/{session_id}")
async def get_risk_assessment(session_id: str):
    """Generates an AI-driven Corporate Risk Score for a notice."""
    session_data = get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
        
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    prompt = f"""You are a Senior Corporate Defense Lawyer in India. 
    Analyze this consumer complaint from a business perspective.
    FACTS: {json.dumps(session_data['facts'])}
    
    Return a JSON object with:
    1. risk_score: (0 to 100, where 100 is certain loss in court)
    2. legal_vulnerability: (The weakest point in the company's defense)
    3. recommendation: (Should they Refund, Repair, or Fight?)
    4. estimated_cost: (Potential cost if this goes to District Commission)
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=genai.types.GenerateContentConfig(response_mime_type="application/json")
    )
    import json
    return json.loads(response.text)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Day 2: Persistent LangGraph Integration"""
    try:
        from agent import intake_agent
        
        # 1. Retrieve or Initialize State for this specific user session
        session_id = request.session_id
        current_state = get_session(session_id)
        if not current_state:
            current_state = {
                "session_id": session_id,
                "chat_history": [],
                "facts": {},
                "is_complete": False,
                "latest_response": ""
            }
        
        # 2. Append the user's new message to the memory
        current_state["chat_history"].append({"role": "user", "text": request.message})
        
        # 3. RUN THE AGENTIC BRAIN (LangGraph Pipeline)
        # This analyzes the history, extracts facts to JSON, and generates a smart response
        new_state = intake_agent.invoke(current_state)
        
        # 4. Append the AI's response to history and save state
        new_state["chat_history"].append({"role": "ai", "text": new_state.get("latest_response", "")})
        save_session(new_state)
        
        return ChatResponse(
            reply=new_state.get("latest_response", "I could not process that."),
            status="complete" if new_state.get("is_complete") else "active"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload_receipt")
async def upload_receipt(session_id: str, file: UploadFile = File(...)):
    """Day 2: Vision OCR Endpoint that syncs with the Session Brain"""
    try:
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        file_bytes = await file.read()
        prompt = """You are a Forensic AI Legal Clerk. Analyze this Indian retail receipt or invoice.
        Extract and return exactly these 4 facts in JSON format:
        {
          "opponent_name": "Exact name of the company",
          "incident_date": "Exact transaction date",
          "dispute_amount": "Total Amount",
          "product_name": "Short summary of item"
        }
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt, 
                genai.types.Part.from_bytes(data=file_bytes, mime_type=file.content_type)
            ],
            config=genai.types.GenerateContentConfig(response_mime_type="application/json")
        )
        import json
        extracted_data = json.loads(response.text)
        
        # SYNC WITH SESSION: Load current state and inject these new facts
        current_state = get_session(session_id)
        if not current_state:
            current_state = {"session_id": session_id, "chat_history": [], "facts": {}, "is_complete": False, "latest_response": ""}
        
        # Inject extracted facts into the persistent state
        current_state["facts"].update(extracted_data)
        save_session(current_state)
        
        return {"extracted_text": response.text.strip(), "message": "Bill details successfully synced with your case."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download_notice/{session_id}")
async def download_notice(session_id: str):
    """Day 3: Generate and serve the PDF"""
    from database import get_session
    session_data = get_session(session_id)
    if not session_data or not session_data.get("is_complete"):
        raise HTTPException(status_code=400, detail="Case is not complete yet.")
    
    from drafter import draft_legal_text, create_pdf
    facts = session_data["facts"]
    pdf_path = f"nyaya_notice_{session_id}.pdf"
    
    # Generate exactly what happens in Day 3
    draft_text = draft_legal_text(facts)
    create_pdf(draft_text, pdf_path, session_id=session_id)
    
    return FileResponse(path=pdf_path, media_type='application/pdf', filename="Nyaya_Voice_Formal_Notice.pdf")

if __name__ == "__main__":
    import uvicorn
    # Make sure to run this file or use the command: uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
