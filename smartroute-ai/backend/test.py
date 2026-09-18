from analyzer import ComplexityAnalyzer
from router import RoutingEngine
from ollama_client import query_tinyllama

print("--- Testing SmartRoute AI Core Engine ---")

query = "What is Java?"
print(f"\n[1] Query: '{query}'")

# 1. Analyze Complexity
analysis = ComplexityAnalyzer().analyze(query)
print(f"\n[2] Analysis Result:\n{analysis}")

# 2. Route Model
model_info = RoutingEngine().route(analysis["score"])
print(f"\n[3] Routing Result:\n{model_info}")

# 3. Execute Query if TinyLlama is selected
if model_info["selected_model"] == "tinyllama":
    print("\n[4] Routing to TinyLlama...")
    response = query_tinyllama(query)
    print("\n[5] Final Response:")
    print(response["response"])
else:
    print(f"\n[4] Routed to {model_info['selected_model']} (Gemini connection not tested here)")