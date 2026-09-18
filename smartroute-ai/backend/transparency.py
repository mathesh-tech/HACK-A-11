"""
MODULE 6 - Transparency Engine

Provides a clear explanation of why a specific model was selected
by the routing engine, enhancing trust and auditability.
"""

class TransparencyEngine:
    def explain(self, difficulty: str, score: int, model: str) -> dict:
        """
        Generates a transparent explanation for model routing decisions.
        """
        model_name = model.lower()
        
        # Determine explanation based on selected model and difficulty
        if model_name == "tinyllama":
            reason = "Simple factual query detected. TinyLlama is sufficient and cost-effective."
        elif model_name == "gemini":
            if difficulty.lower() == "medium":
                reason = "Moderate reasoning required. Routed to Gemini for reliable quality."
            else:
                reason = "Complex reasoning required. Routed to Gemini for stronger capabilities."
        else:
            reason = f"Routed to {model} based on the query complexity score."

        return {
            "difficulty": difficulty,
            "score": score,
            "selected_model": model,
            "routing_reason": reason
        }

# Helper function for quick functional use
def generate_explanation(difficulty: str, score: int, model: str) -> dict:
    return TransparencyEngine().explain(difficulty, score, model)
