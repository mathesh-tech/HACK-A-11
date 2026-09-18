"""
MODULE 4 - Connector B: Gemini Client

Communicates with the Gemini API.
Reads GEMINI_API_KEY from .env.
Handles errors, timeouts, and empty responses gracefully.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

def query_gemini(prompt: str) -> dict:
    if not GEMINI_API_KEY:
        error_msg = "[Error: No GEMINI_API_KEY provided in .env]"
        return {"response": error_msg, "text": error_msg, "source": "gemini-mock"}

    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=15, # Handle timeouts
        )
        resp.raise_for_status()
        data = resp.json()
        
        # Safely extract text to handle potential missing fields
        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )
        
        text = text.strip()
        if not text:
            # Handle empty responses
            empty_msg = "[Gemini returned an empty response]"
            return {"response": empty_msg, "text": empty_msg, "source": "gemini-live"}
            
        return {"response": text, "text": text, "source": "gemini-live"}
        
    except requests.exceptions.Timeout:
        timeout_msg = "[Error: Gemini API request timed out]"
        return {"response": timeout_msg, "text": timeout_msg, "source": "gemini-error"}
    except Exception as e:
        # Handle general errors
        error_msg = f"[Error: Gemini API call failed - {e}]"
        return {"response": error_msg, "text": error_msg, "source": "gemini-error"}
