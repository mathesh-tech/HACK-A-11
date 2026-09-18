import time
import uuid
import logging
from flask import Blueprint, request, jsonify

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

@query_bp.route("/api/query", methods=["POST"])
def process_query():
    """
    POST /api/query
    Integrates all modules into a single workflow with robust error handling.
    """
    try:
        # 1. Receive JSON request
        payload = request.get_json(force=True) or {}
        query = (payload.get("query") or "").strip()

        # 2. Validate input
        if not query:
            return jsonify({
                "success": False,
                "error": "Missing or empty 'query' field in request body."
            }), 400

        t_start = time.time()

        # 3 & 4. Run Complexity Analyzer
        try:
            analysis = analyzer.analyze(query)
        except Exception as e:
            logging.error(f"Analyzer failed: {e}")
            return jsonify({"success": False, "error": "Complexity analyzer failed."}), 500

        # 5. Select model using router
        try:
            routing = router_engine.route(analysis["score"])
            selected_model = routing["selected_model"]
        except Exception as e:
            logging.error(f"Router failed: {e}")
            return jsonify({"success": False, "error": "Routing engine failed."}), 500

        routing_time_ms = round((time.time() - t_start) * 1000, 2)

        # 6 & 7. Call LLM Client
        gen_start = time.time()
        try:
            if selected_model == "tinyllama":
                model_response = ollama_client.query_tinyllama(query)
            else:
                model_response = gemini_client.query_gemini(query)
                
            # Handle potential failure response format from clients
            if not model_response or ("response" not in model_response and "text" not in model_response):
                raise ValueError("Invalid response format from model client.")
                
            answer_text = model_response.get("response", model_response.get("text", ""))
        except Exception as e:
            logging.error(f"Model generation failed: {e}")
            return jsonify({"success": False, "error": f"Failed to generate response using {selected_model}."}), 502

        generation_time_ms = round((time.time() - gen_start) * 1000, 2)

        # 8. Calculate cost
        try:
            cost_info = cost_engine.calculate_cost(selected_model)
        except Exception as e:
            logging.error(f"Cost engine failed: {e}")
            cost_info = {"actual_cost": 0, "baseline_cost": 0, "saving_percentage": 0}

        # 9. Generate transparency explanation
        try:
            transparency_info = generate_transparency(
                difficulty=analysis["difficulty"],
                score=analysis["score"],
                selected_model=selected_model
            )
        except Exception as e:
            logging.error(f"Transparency engine failed: {e}")
            transparency_info = {"routing_reason": "Routing logic applied."}

        # Save to DB history (Best effort)
        record_id = str(uuid.uuid4())
        try:
            record = {
                "id": record_id,
                "timestamp": time.time(),
                "query": query,
                "difficulty": analysis["difficulty"],
                "score": analysis["score"],
                "confidence": analysis.get("confidence", 100),
                "selected_model": selected_model,
                "routing_reason": transparency_info["routing_reason"],
                "routing_time_ms": routing_time_ms,
                "generation_time_ms": generation_time_ms,
                "actual_cost": cost_info.get("actual_cost", 0),
                "baseline_cost": cost_info.get("baseline_cost", 0.10),
                "savings_pct": cost_info.get("saving_percentage", 0),
                "currency": "INR",
                "override_mode": "auto",
                "response_preview": answer_text[:400],
                "model_source": model_response.get("source", "unknown"),
            }
            models.save_query(record)
        except Exception as e:
            logging.warning(f"Failed to log query to DB: {e}")

        # 10. Return structured JSON response exactly matching requirements
        return jsonify({
            "success": True,
            "query": query,
            "answer": answer_text,
            "difficulty": analysis["difficulty"],
            "score": analysis["score"],
            "model_used": selected_model,
            "routing_reason": transparency_info["routing_reason"],
            "cost_analysis": {
                "actual_cost": cost_info.get("actual_cost", 0),
                "baseline_cost": cost_info.get("baseline_cost", 0.10),
                "saving_percentage": cost_info.get("saving_percentage", 0)
            },
            # Helpful extra meta fields for frontend UI
            "timing": {
                "routing_time_ms": routing_time_ms,
                "generation_time_ms": generation_time_ms,
                "total_time_ms": round(routing_time_ms + generation_time_ms, 2)
            },
            "id": record_id
        }), 200

    except Exception as e:
        logging.error(f"Unexpected error in /query endpoint: {e}")
        return jsonify({"success": False, "error": "Internal server error."}), 500
