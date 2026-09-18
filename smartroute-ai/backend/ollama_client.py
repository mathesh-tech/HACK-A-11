"""
MODULE 4 - Connector A: TinyLlama via Ollama

Talks to a locally running Ollama server. Includes production-ready
error handling for timeouts and connection failures.
"""
import requests

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "tinyllama"

def query_tinyllama(prompt: str) -> dict:
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        # Connect to Ollama server with timeout handling
        resp = requests.post(url, json=payload, timeout=20)
        resp.raise_for_status()
        
        data = resp.json()
        answer = data.get("response", "").strip()
        
        if not answer:
            error_msg = "[Error: Ollama returned an empty response]"
            return {
                "success": False,
                "response": error_msg,
                "text": error_msg,
                "source": "tinyllama-empty"
            }
            
        return {
            "success": True,
            "response": answer,
            "text": answer, # Retained for backward compatibility with router
            "source": "tinyllama-live"
        }
        
    except requests.exceptions.ConnectionError:
        error_msg = f"[Error: Could not connect to Ollama on {OLLAMA_URL}. Is it running?]"
        return {
            "success": False,
            "response": error_msg,
            "text": error_msg,
            "source": "tinyllama-error"
        }
    except requests.exceptions.Timeout:
        error_msg = "[Error: Connection to Ollama server timed out]"
        return {
            "success": False,
            "response": error_msg,
            "text": error_msg,
            "source": "tinyllama-error"
        }
    except Exception as e:
        error_msg = f"[Error: Unexpected failure while calling Ollama - {e}]"
        return {
            "success": False,
            "response": error_msg,
            "text": error_msg,
            "source": "tinyllama-error"
        }
