# backend/flask_app.py

from flask import Flask
from backend.src.api.classify_controller_flask import classify_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(classify_bp, url_prefix='/api/classify')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
