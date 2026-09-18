"""
MODULE 3 - Routing Engine

Selects the best LLM based on the difficulty score.
Routing Rules:
- Easy (0-3): TinyLlama
- Medium (4-6): Gemini
- Hard (7-10): Gemini
"""

class RoutingEngine:
    def route(self, score: int, override: str = "auto") -> dict:
        # Handle manual overrides first
        if override == "tinyllama":
            return {
                "selected_model": "tinyllama",
                "reason": "Manual override: user forced TinyLlama"
            }
        if override == "gemini":
            return {
                "selected_model": "gemini",
                "reason": "Manual override: user forced Gemini"
            }

        # Automatic Routing based on difficulty score
        if score <= 3:
            return {
                "selected_model": "tinyllama",
                "reason": "Simple query. TinyLlama is sufficient and cost-effective."
            }
        elif score <= 6:
            return {
                "selected_model": "gemini",
                "reason": "Moderate reasoning required. Routed to Gemini for reliable quality."
            }
        else:
            return {
                "selected_model": "gemini",
                "reason": "Complex reasoning required"
            }
