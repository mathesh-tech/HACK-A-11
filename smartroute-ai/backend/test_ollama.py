import requests
import json

def test_ollama_connection():
    print("-" * 32)
    print("Testing TinyLlama Connection...")
    print("-" * 32)
    print()

    # 1. Define the API endpoint for the local Ollama server
    url = "http://localhost:11434/api/generate"
    
    # 2. Set up the payload according to requirements
    payload = {
        "model": "tinyllama",
        "prompt": "What is polymorphism in Java?",
        "stream": False
    }

    try:
        # 3. Send the POST request to the Ollama server (with timeout)
        response = requests.post(url, json=payload, timeout=15)
        
        # Raise an exception for bad HTTP status codes
        response.raise_for_status()
        
        # 4. Parse the JSON response
        data = response.json()
        
        # 5. Extract the generated answer
        answer = data.get("response", "").strip()
        
        # 6. Check for an empty response
        if not answer:
            print("Error: The Ollama server returned an empty response.")
            return

        # 7. Print only the generated answer
        print("Model Response:")
        print(answer)
        print()
        
        print("-" * 32)
        print("Connection Successful")
        print("-" * 32)

    except requests.exceptions.ConnectionError:
        # Handle case where Ollama server is not running
        print("Error: Could not connect to the Ollama server. Is it running?")
    except requests.exceptions.Timeout:
        # Handle connection timeout
        print("Error: Connection to the Ollama server timed out.")
    except json.JSONDecodeError:
        # Handle invalid JSON response
        print("Error: Received invalid JSON from the Ollama server.")
    except requests.exceptions.RequestException as e:
        # Handle any other request-related errors
        print(f"Error: An unexpected network error occurred: {e}")
    except Exception as e:
        # Handle general unexpected errors
        print(f"Error: An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_ollama_connection()