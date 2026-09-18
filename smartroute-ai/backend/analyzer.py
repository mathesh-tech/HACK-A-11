"""
MODULE 2 - Complexity Analyzer

Analyzes user queries and classifies their difficulty using the
Query Complexity Index (QCI) formula:
QCI = (Query Length × 0.2) + (Technical Keywords × 2) + (Multi-step Tasks × 3) + (Reasoning Requirement × 4)
"""
import re

MEDIUM_KEYWORDS = ["summarize", "compare", "explain briefly", "list", "outline"]
HARD_KEYWORDS = ["design", "architecture", "scalable", "optimize", "debug", "implement", "derive", "proof"]

class ComplexityAnalyzer:
    def analyze(self, query: str) -> dict:
        text = query.lower().strip()
        length = len(text.split())

        # Extract features for QCI
        technical_keywords_count = sum(text.count(kw) for kw in HARD_KEYWORDS)
        multi_step_count = text.count(" and ") + text.count("\n") + max(text.count("?") - 1, 0)
        reasoning_keywords_count = sum(text.count(kw) for kw in MEDIUM_KEYWORDS)

        # Apply QCI Formula
        query_length_factor = length * 0.2
        technical_factor = technical_keywords_count * 2
        multistep_factor = multi_step_count * 3
        reasoning_factor = reasoning_keywords_count * 4

        qci_score = query_length_factor + technical_factor + multistep_factor + reasoning_factor
        
        # Round and cap if necessary to ensure it's easily mapped, though >= 7 handles unbounded.
        qci_rounded = round(qci_score)
        qci_final = max(0, min(10, qci_rounded)) # Cap at 10 for consistency

        # Determine difficulty based on QCI
        if qci_rounded <= 3:
            difficulty = "Easy"
        elif qci_rounded <= 6:
            difficulty = "Medium"
        else:
            difficulty = "Hard"

        # Generate explanation based on significant factors
        explanation_parts = []
        if query_length_factor >= 2:
            explanation_parts.append(f"Length adds {round(query_length_factor, 1)} pts")
        if technical_factor > 0:
            explanation_parts.append(f"Technical terms add {technical_factor} pts")
        if multistep_factor > 0:
            explanation_parts.append(f"Multi-step tasks add {multistep_factor} pts")
        if reasoning_factor > 0:
            explanation_parts.append(f"Reasoning requirements add {reasoning_factor} pts")

        explanation = ", ".join(explanation_parts) if explanation_parts else "Short, simple factual query"

        # Calculate a basic confidence score (example heuristic)
        confidence = 90 if length > 5 else 60

        return {
            "difficulty": difficulty,
            "score": qci_final, # Returning capped score 0-10
            "qci_raw_score": round(qci_score, 2), # Raw QCI just in case
            "reason": explanation,
            "explanation": explanation,
            "confidence": confidence,
            "signals": explanation_parts # Keep for backward compatibility
        }
