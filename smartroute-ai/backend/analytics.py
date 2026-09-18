"""
MODULE 7 - Admin Dashboard aggregation
"""
import models


def get_stats():
    rows = models.get_all()
    total = len(rows)

    if total == 0:
        return {
            "total_queries": 0,
            "easy_queries": 0,
            "medium_queries": 0,
            "hard_queries": 0,
            "most_used_model": None,
            "model_usage": {"tinyllama": 0, "gemini": 0},
            "model_usage_pct": {"tinyllama": 0, "gemini": 0},
            "total_actual_cost": 0,
            "total_baseline_cost": 0,
            "total_savings": 0,
            "average_savings_pct": 0,
            "average_response_time_ms": 0,
        }

    easy = sum(1 for r in rows if r["difficulty"] == "Easy")
    medium = sum(1 for r in rows if r["difficulty"] == "Medium")
    hard = sum(1 for r in rows if r["difficulty"] == "Hard")

    tinyllama_count = sum(1 for r in rows if r["selected_model"] == "tinyllama")
    gemini_count = sum(1 for r in rows if r["selected_model"] == "gemini")
    most_used = "tinyllama" if tinyllama_count >= gemini_count else "gemini"

    total_actual = sum(r["actual_cost"] for r in rows)
    total_baseline = sum(r["baseline_cost"] for r in rows)
    total_savings = round(total_baseline - total_actual, 4)
    avg_savings_pct = round(sum(r["savings_pct"] for r in rows) / total, 1)
    avg_response_time = round(
        sum((r["routing_time_ms"] or 0) + (r["generation_time_ms"] or 0) for r in rows) / total, 1
    )

    return {
        "total_queries": total,
        "easy_queries": easy,
        "medium_queries": medium,
        "hard_queries": hard,
        "most_used_model": most_used,
        "model_usage": {"tinyllama": tinyllama_count, "gemini": gemini_count},
        "model_usage_pct": {
            "tinyllama": round(tinyllama_count / total * 100, 1),
            "gemini": round(gemini_count / total * 100, 1),
        },
        "total_actual_cost": round(total_actual, 4),
        "total_baseline_cost": round(total_baseline, 4),
        "total_savings": total_savings,
        "average_savings_pct": avg_savings_pct,
        "average_response_time_ms": avg_response_time,
    }
