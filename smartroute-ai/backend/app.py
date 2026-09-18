"""
SmartRoute AI - Backend
"Right Model. Right Cost."

Flask API gateway that analyzes incoming queries, routes them to the
cheapest capable LLM (TinyLlama via Ollama, or Gemini 2.5 Flash),
tracks cost/savings, and serves an admin dashboard.
"""
import time
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

from analyzer import ComplexityAnalyzer
import models
import analytics
from routes import query_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(query_bp)

models.init_db()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "SmartRoute AI"})


@app.route("/api/history", methods=["GET"])
def history():
    limit = int(request.args.get("limit", 50))
    return jsonify(models.get_history(limit))


@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(analytics.get_stats())


@app.route("/api/reset", methods=["POST"])
def reset():
    models.reset_db()
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

