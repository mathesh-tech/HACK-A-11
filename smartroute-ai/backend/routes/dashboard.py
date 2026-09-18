from flask import Blueprint, request, jsonify
from . import dashboard_bp
import models
import analytics

@dashboard_bp.route("/api/history", methods=["GET"])
def history():
    limit = int(request.args.get("limit", 50))
    return jsonify(models.get_history(limit))

@dashboard_bp.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(analytics.get_stats())

@dashboard_bp.route("/api/reset", methods=["POST"])
def reset():
    models.reset_db()
    return jsonify({"status": "reset"})
