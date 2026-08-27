import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Ensure we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
os.environ["GEMINI_API_KEY"] = "dummy_test_key"
os.environ["SARVAM_API_KEY"] = "dummy_test_key"

from main import app
from database import get_session, save_session, update_session_facts
from speech import SarvamSpeechToText

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_database_fallback():
    # Test save and get
    session_id = "test_session_123"
    state = {
        "session_id": session_id,
        "chat_history": [{"role": "user", "text": "hello"}],
        "facts": {"user_name": "Test User"},
        "is_complete": False,
        "latest_response": "Hi there"
    }
    save_session(state)
    
    retrieved = get_session(session_id)
    assert retrieved is not None
    assert retrieved["session_id"] == session_id
    assert len(retrieved["chat_history"]) == 1
    assert retrieved["facts"]["user_name"] == "Test User"
    
    # Test surgical update
    update_session_facts(session_id, {"dispute_amount": "500"})
    updated = get_session(session_id)
    assert updated["facts"]["dispute_amount"] == "500"
    assert updated["facts"]["user_name"] == "Test User"

@patch('speech.requests.post')
def test_sarvam_stt_client(mock_post):
    stt = SarvamSpeechToText(api_key="test_key")
    
    # Mock valid response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "transcript": "Hello this is a test.",
        "language_code": "en",
        "request_id": "req-123"
    }
    mock_post.return_value = mock_response
    
    result = stt.transcribe(b"dummy_audio_bytes")
    assert result["success"] is True
    assert result["transcript"] == "Hello this is a test."
    
    # Mock error response
    mock_response_err = MagicMock()
    mock_response_err.status_code = 401
    mock_response_err.text = "Unauthorized"
    mock_post.return_value = mock_response_err
    
    result_err = stt.transcribe(b"dummy_audio_bytes")
    assert result_err["success"] is False
    assert "Unauthorized" in result_err["error"]

@patch('main.stt_client.transcribe')
def test_api_transcribe(mock_transcribe):
    mock_transcribe.return_value = {
        "success": True,
        "transcript": "Mocked transcript",
        "language_code": "en",
        "request_id": "req-123"
    }
    
    files = {'file': ('audio.wav', b'dummy_bytes', 'audio/wav')}
    data = {'mode': 'translate', 'language_code': 'unknown'}
    
    response = client.post("/api/transcribe", files=files, data=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    assert res_data["transcript"] == "Mocked transcript"

@patch('agent.intake_agent.invoke')
def test_api_chat(mock_invoke):
    session_id = "test_chat_session"
    
    # Mock the LLM graph output
    mock_invoke.return_value = {
        "session_id": session_id,
        "chat_history": [{"role": "user", "text": "hello"}, {"role": "ai", "text": "How can I help?"}],
        "facts": {},
        "is_complete": False,
        "latest_response": "How can I help?"
    }
    
    response = client.post("/api/chat", json={
        "message": "hello",
        "session_id": session_id
    })
    
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["reply"] == "How can I help?"
    assert res_data["status"] == "active"
