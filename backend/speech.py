import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"


class SarvamSpeechToText:
    """Client for Sarvam AI Indic Speech-to-Text (Saaras v3)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or SARVAM_API_KEY
        if not self.api_key:
            print("WARNING: SARVAM_API_KEY is not set. STT calls will fail until configured.")

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        mode: str = "translate",
        language_code: str = "unknown"
    ) -> Dict[str, Any]:
        """
        Transcribe or translate an audio file using Sarvam AI.
        
        :param audio_bytes: Raw binary bytes of the audio file.
        :param filename: Filename with extension (e.g. .wav, .mp3, .webm, .ogg).
        :param mode: 'translate' (converts Indic speech to English) or 'transcribe' (native script).
        :param language_code: BCP-47 code or 'unknown' for automatic detection.
        :return: Dict containing 'transcript', 'language_code', and 'success' flag.
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "SARVAM_API_KEY is missing. Please set it in your .env file.",
                "transcript": "",
                "language_code": None
            }

        headers = {
            "api-subscription-key": self.api_key
        }

        # Match content type or fallback to octet-stream
        files = {
            "file": (filename, audio_bytes)
        }
        
        data = {
            "model": "saaras:v3",
            "mode": mode,
            "language_code": language_code
        }

        try:
            response = requests.post(
                SARVAM_STT_URL,
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "transcript": result.get("transcript", "").strip(),
                    "language_code": result.get("language_code"),
                    "request_id": result.get("request_id")
                }
            else:
                return {
                    "success": False,
                    "error": f"Sarvam API Error ({response.status_code}): {response.text}",
                    "transcript": "",
                    "language_code": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"STT Request failed: {str(e)}",
                "transcript": "",
                "language_code": None
            }
