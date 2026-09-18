"""
MODULE 5 - Cost Estimation Engine

Calculates estimated flat cost of the routed call vs. a GPT baseline.
Rates are fixed per request (INR) as specified.
"""

# Flat rates in INR per request
RATES = {
    "tinyllama": 0.00,
    "gemini": 0.01,
    "gpt_baseline": 0.10,
}

class CostEngine:
    def calculate_cost(self, model: str) -> dict:
        """
        Calculates cost and savings against a baseline model.
        Returns actual_cost, baseline_cost, and saving_percentage.
        """
        # Handle unknown models by defaulting to gemini
        model_key = model.lower()
        if model_key not in RATES:
            model_key = "gemini"

        actual_cost = RATES[model_key]
        baseline_cost = RATES["gpt_baseline"]

        # Calculate saving percentage
        if baseline_cost > 0:
            saving_percentage = round(((baseline_cost - actual_cost) / baseline_cost) * 100)
        else:
            saving_percentage = 0

        return {
            "actual_cost": actual_cost,
            "baseline_cost": baseline_cost,
            "saving_percentage": saving_percentage,
            # Legacy mapping for backwards compatibility with the router if needed
            "savings_pct": saving_percentage 
        }
