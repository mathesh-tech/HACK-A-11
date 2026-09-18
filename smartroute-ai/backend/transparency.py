"""
MODULE 6 - Transparency Engine

Provides clear explanations for why a specific AI model was selected.
Ensures users and judges understand the routing decision instead of seeing a black-box output.
"""

def generate_transparency(difficulty: str, score: int, selected_model: str) -> dict:
    """
    Generates a structured, human-readable explanation for model routing decisions.
    Handles 'Easy', 'Medium', 'Hard' difficulties and defaults gracefully for unknown inputs.
    """
    # Normalize difficulty for robust handling
    diff_lower = difficulty.lower().strip() if isinstance(difficulty, str) else ""

    # Determine explanation based on difficulty and model selection
    if diff_lower == "easy":
        reason = "Simple factual query detected. TinyLlama selected to minimize cost and provide fast responses."
    elif diff_lower == "medium":
        reason = "Moderate reasoning required. Gemini selected to provide better contextual understanding."
    elif diff_lower == "hard":
        reason = "Complex reasoning detected. Gemini selected for advanced processing capabilities."
    else:
        # Graceful fallback for invalid difficulty values
        reason = f"Query complexity evaluated. {selected_model} selected to optimize for performance and cost."
        difficulty = "Unknown" # Standardize invalid input

    return {
        "difficulty": difficulty,
        "score": score,
        "selected_model": selected_model,
        "routing_reason": reason
    }

