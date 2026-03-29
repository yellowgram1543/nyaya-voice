import os
import json
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from google import genai
from pydantic import BaseModel, Field

# We use the new Gemini native SDK installed earlier
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. State Tracking: This is the Agent's "Persistent Memory"
class CaseState(TypedDict):
    session_id: str
    chat_history: List[dict]  # format: [{'role': 'user', 'text': 'I got scammed'}]
    facts: dict               # Our 6 mandatory facts
    is_complete: bool         # Flips to True when all 6 facts are collected
    latest_response: str      # What the AI will whisper to the user next

# 2. Structured output validation to guarantee Gemini outputs a perfect JSON object
class FactExtraction(BaseModel):
    user_name: Optional[str] = Field(description="The user's full name, if explicitly mentioned.")
    user_city: Optional[str] = Field(description="The city where the user resides (e.g. Mumbai, Bangalore).")
    user_pincode: Optional[str] = Field(description="The 6-digit residential Pincode of the user (e.g. 400001).")
    opponent_name: Optional[str] = Field(description="The company, service, or person being sued.")
    opponent_address: Optional[str] = Field(description="The registered office address of the opponent/company.")
    incident_date: Optional[str] = Field(description="The date or time frame the issue occurred.")
    dispute_amount: Optional[str] = Field(description="The exact monetary amount involved (e.g. 1500 INR).")
    core_issue: Optional[str] = Field(description="A 1-sentence summary of what went wrong.")
    desired_resolution: Optional[str] = Field(description="What the user specifically wants (e.g. refund, replacement).")
    ai_response_to_user: str = Field(description="The conversational text to say back to the user to gather missing facts politely.")

# 3. The LangGraph Node
def intake_node(state: CaseState) -> CaseState:
    # Build conversation context
    history_text = ""
    for msg in state.get('chat_history', []):
        role = "User" if msg['role'] == "user" else "AI"
        history_text += f"{role}: {msg['text']}\n"
        
    prompt = f"""You are the Nyaya-Voice Intake AI, a polite expert in Indian Consumer Protection Law.
    Your mission is to perform a gap-analysis. We need EXACTLY 9 facts from the user to draft a legal notice.
    
    Your internal state of the facts we already have so far:
    {json.dumps(state.get('facts', {}))}
    
    Conversation History:
    {history_text}
    
    1. CRITICAL: Seamlessly comprehend multiple Indian languages including 'Hinglish' (mixed Hindi and English), Telugu, Kannada, and regional dialect slang.
       Automatically translate these informal or regional inputs into formal, legally accurate English facts when updating your internal state.
    2. Read the history and update your internal state if the user provided new facts.
    3. If facts are STILL MISSING, your `ai_response_to_user` MUST politely ask the user for them. Interrogate naturally. **CRITICAL RULE:** Actively mirror the user's language. If they spoke in Hinglish, Telugu, or Kannada, reply in that exact same language to make them comfortable.
       Specifically ensure we get the 'user_city', 'user_pincode' (6-digits), and the 'opponent_address' (Registered Office) for a formal legal notice.
    4. If ALL 9 FACTS are present, politely confirm that the intake is complete and you are ready to draft the formal PDF notice.
    """
    
    # We force Gemini to output strictly matching our Pydantic FactExtraction schema
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FactExtraction,
        ),
    )
    
    try:
        data = json.loads(response.text)
    except:
        data = {}
    
    # Merge existing facts with newly discovered facts
    current_facts = state.get("facts", {})
    new_facts = {
        "user_name": data.get("user_name"),
        "user_city": data.get("user_city"),
        "user_pincode": data.get("user_pincode"),
        "opponent_name": data.get("opponent_name"),
        "opponent_address": data.get("opponent_address"),
        "incident_date": data.get("incident_date"),
        "dispute_amount": data.get("dispute_amount"),
        "core_issue": data.get("core_issue"),
        "desired_resolution": data.get("desired_resolution")
    }
    
    for k, v in new_facts.items():
        if v and v.strip() != "":
            current_facts[k] = v
            
    # Check if we hit the Day 2 Milestone (all 9 collected!)
    mandatory_keys = ["user_name", "user_city", "user_pincode", "opponent_name", "opponent_address", "incident_date", "dispute_amount", "core_issue", "desired_resolution"]
    is_complete = all(k in current_facts and current_facts[k] for k in mandatory_keys)

    return {
        "chat_history": state['chat_history'],
        "facts": current_facts,
        "is_complete": is_complete,
        "latest_response": data.get("ai_response_to_user", "I encountered an error parsing your response.")
    }

# 4. Compile the Graph
workflow = StateGraph(CaseState)
workflow.add_node("intake", intake_node)
workflow.set_entry_point("intake")
workflow.add_edge("intake", END) 

# Export the compiled agent
intake_agent = workflow.compile()
