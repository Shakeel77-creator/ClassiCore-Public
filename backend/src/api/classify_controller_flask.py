from flask import Blueprint, request, jsonify
from backend.src.services.classify_service import ClassifyService

classify_bp = Blueprint('classify_bp', __name__)
classifier = ClassifyService()

@classify_bp.route('/predict', methods=['POST'])
def classify_product_api():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid input format. Expected JSON object."}), 400

        product_name = data.get("product_name")

        if not product_name:
            return jsonify({"error": "Missing 'product_name' in request body."}), 400

        results = classifier.classify_product(product_name)
        return jsonify({"status": "success", "data": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
