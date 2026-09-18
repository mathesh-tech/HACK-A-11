import time
import uuid
from flask import Blueprint, request, jsonify

# We import the instances from the main app or initialize them here.
# For simplicity, we can initialize them here or import from a services module.
# Let's import the engine classes and initialize them in the blueprint or app.
from analyzer import ComplexityAnalyzer
from router import RoutingEngine
from cost_engine import CostEngine
from transparency import generate_transparency
import ollama_client
import gemini_client
import models
from . import query_bp

analyzer = ComplexityAnalyzer()
router_engine = RoutingEngine()
cost_engine = CostEngine()

@query_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    Core pipeline:
    Query -> Complexity Analyzer -> Difficulty Scoring -> LLM Router
    -> Model Selection -> Response Generator -> logged to DB
    """
    payload = request.get_json(force=True) or {}
    query = (payload.get("query") or "").strip()
    override = payload.get("override", "auto")  # auto | tinyllama | gemini

    if not query:
        return jsonify({"error": "query is required"}), 400

    t_start = time.time()

    # MODULE 2 - Complexity Analyzer
    analysis = analyzer.analyze(query)

    # MODULE 3 - Routing Engine (respects manual override)
    routing = router_engine.route(analysis["score"], override=override)
    routing_time_ms = round((time.time() - t_start) * 1000, 2)

    # MODULE 4 - Model Connectors
    gen_start = time.time()
    if routing["selected_model"] == "tinyllama":
        model_response = ollama_client.query_tinyllama(query)
    else:
        model_response = gemini_client.query_gemini(query)
    generation_time_ms = round((time.time() - gen_start) * 1000, 2)

    # MODULE 5 - Cost Engine
    cost_info = cost_engine.calculate_cost(routing["selected_model"])

    # MODULE 6 - Transparency Engine
    transparency_info = generate_transparency(
        difficulty=analysis["difficulty"],
        score=analysis["score"],
        selected_model=routing["selected_model"]
    )

    record = {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "query": query,
        "difficulty": analysis["difficulty"],
        "score": analysis["score"],
        "confidence": analysis["confidence"],
        "selected_model": routing["selected_model"],
        "routing_reason": transparency_info["routing_reason"],
        "routing_time_ms": routing_time_ms,
        "generation_time_ms": generation_time_ms,
        "actual_cost": cost_info["actual_cost"],
        "baseline_cost": cost_info["baseline_cost"],
        "savings_pct": cost_info["saving_percentage"],
        "currency": "INR",
        "override_mode": override,
        "response_preview": model_response["text"][:400],
        "model_source": model_response["source"],
    }
    models.save_query(record)

    return jsonify({
        "response": model_response.get("response", model_response.get("text")),
        "model_source": model_response["source"],
        "analysis": analysis,
        "routing": routing,
        "cost": cost_info,
        "transparency": transparency_info,
        "timing": {
            "routing_time_ms": routing_time_ms,
            "generation_time_ms": generation_time_ms,
            "total_time_ms": round(routing_time_ms + generation_time_ms, 2),
        },
        "id": record["id"],
    })
