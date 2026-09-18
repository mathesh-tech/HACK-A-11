"""
MODULE 4 - Connector B: Gemini Client

Communicates with the Gemini API.
Reads GEMINI_API_KEY from .env robustly.
Handles errors, timeouts, and empty responses gracefully.
Includes a robust retry mechanism for 503 errors.
"""
import os
import time
import requests
from dotenv import load_dotenv

# 1. Resolve absolute path to .env specifically in the backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Force-load .env from exact location
load_dotenv(dotenv_path=ENV_PATH)

GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

def query_gemini(prompt: str) -> dict:
    # 2. Fetch the key dynamically inside the function
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    # 3. Debug prints as requested
    print("DEBUG GEMINI KEY =", api_key)
    print("DEBUG ENV PATH =", ENV_PATH)
    
    if not api_key:
        error_msg = f"[Error: No GEMINI_API_KEY provided in .env at {ENV_PATH}]"
        print(error_msg)
        return {"response": error_msg, "text": error_msg, "source": "gemini-mock"}

    url = f"{GEMINI_URL}?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    # Retry logic (up to 3 times)
    for attempt in range(1, 4):
        try:
            # 4. Print the exact URL being called
            print(f"DEBUG GEMINI URL (Attempt {attempt}) = {GEMINI_URL}?key={api_key[:10]}...")
            
            resp = requests.post(
                url,
                json=payload,
                timeout=15, # Handle timeouts
            )
            
            # If 503, trigger the retry loop instead of jumping to exception block immediately
            if resp.status_code == 503:
                print(f"DEBUG GEMINI HTTP {resp.status_code}: {resp.text}")
                if attempt < 3:
                    print("DEBUG GEMINI: Waiting 2 seconds before retry...")
                    time.sleep(2)
                    continue
                else:
                    error_msg = f"[Error: Gemini API HTTP Error - 503 Service Unavailable (Failed after 3 retries)]"
                    print(error_msg)
                    return {"response": error_msg, "text": error_msg, "source": "gemini-error"}
            
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
            timeout_msg = f"[Error: Gemini API request timed out on attempt {attempt}]"
            print(timeout_msg)
            if attempt < 3:
                time.sleep(2)
                continue
            return {"response": timeout_msg, "text": timeout_msg, "source": "gemini-error"}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"DEBUG 404 FULL RESPONSE BODY:\n{e.response.text}")
            error_msg = f"[Error: Gemini API HTTP Error - {e.response.status_code} {e.response.reason}]"
            print(error_msg)
            return {"response": error_msg, "text": error_msg, "source": "gemini-error"}
        except Exception as e:
            # Handle general errors
            error_msg = f"[Error: Gemini API call failed - {e}]"
            print(error_msg)
            return {"response": error_msg, "text": error_msg, "source": "gemini-error"}
