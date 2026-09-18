"""
MODULE 2 - Complexity Analyzer

Analyzes user queries and classifies their difficulty using the
Query Complexity Index (QCI) formula:
QCI = (Query Length × 0.2) + (Technical Keywords × 2) + (Multi-step Tasks × 3) + (Reasoning Requirement × 4)
"""
import re

MEDIUM_KEYWORDS = ["explain", "describe", "how does", "working of", "architecture", "advantages", "disadvantages", "algorithm"]
HARD_KEYWORDS = ["compare", "analyze", "design", "evaluate", "trade-offs", "multi-step reasoning"]
EASY_KEYWORDS = ["what is", "define"]

class ComplexityAnalyzer:
    def analyze(self, query: str) -> dict:
        text = query.lower().strip()
        length = len(text.split())

        # Count keyword occurrences
        medium_count = sum(1 for kw in MEDIUM_KEYWORDS if kw in text)
        hard_count = sum(1 for kw in HARD_KEYWORDS if kw in text)

        # Adjusted scoring logic to guarantee ranges requested by user:
        # Easy (1-3), Medium (4-6), Hard (7-10)
        
        query_length_factor = length * 0.1
        
        # Medium keywords contribute heavily to push into 4-6 range
        medium_factor = medium_count * 3
        
        # Hard keywords contribute massively to push into 7-10 range
        hard_factor = hard_count * 6

        # Base score of 1.0
        qci_score = 1.0 + query_length_factor + medium_factor + hard_factor
        
        # Cap final score between 1 and 10
        qci_final = int(max(1, min(10, round(qci_score))))

        # Determine difficulty based on QCI
        if qci_final <= 3:
            difficulty = "Easy"
        elif qci_final <= 6:
            difficulty = "Medium"
        else:
            difficulty = "Hard"

        # Requested Debug Prints
        print(f"ANALYZER SCORE = {qci_final}")
        print(f"ANALYZER DIFFICULTY = {difficulty}")

        # Generate explanation based on significant factors
        explanation_parts = []
        if hard_count > 0:
            explanation_parts.append("Complex reasoning detected")
        elif medium_count > 0:
            explanation_parts.append("Explanation or architectural description detected")
        elif length > 15:
            explanation_parts.append("Long multi-part query detected")
        else:
            explanation_parts.append("Simple factual query detected")

        explanation = ", ".join(explanation_parts)

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
