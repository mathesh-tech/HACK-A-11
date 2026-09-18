"""
SmartRoute AI - Backend
"Right Model. Right Cost."

Flask API gateway that uses modular blueprints.
"""
from flask import Flask, jsonify
from flask_cors import CORS

import models
from config import config
from routes import query_bp, dashboard_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(config[config_name])
    
    # Initialize DB
    models.init_db()

    # Health endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "running"})

    # Register blueprints
    app.register_blueprint(query_bp)
    app.register_blueprint(dashboard_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
