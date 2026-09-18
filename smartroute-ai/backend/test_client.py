import json
from ollama_client import query_tinyllama

def test_ollama_client():
    try:
        print("-" * 32)
        print("Testing TinyLlama Client")
        print("-" * 32)
        
        query = "What is Java?"
        print("\nQuery:")
        print(query)
        
        # Call the client function
        result = query_tinyllama(query)
        
        print("\nResponse:")
        # Print the structured dictionary gracefully formatted as JSON
        print(json.dumps(result, indent=4))
        
        print("\n" + "-" * 32)
        print("Test Completed Successfully")
        print("-" * 32)
        
    except Exception as e:
        print(f"\nError: An unexpected exception occurred: {e}")

if __name__ == "__main__":
    test_ollama_client()
