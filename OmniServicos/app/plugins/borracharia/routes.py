from flask import Blueprint, jsonify

borracharia_bp = Blueprint("borracharia", __name__)

@borracharia_bp.route("/test")
def test_borracharia():
    return jsonify({"message": "Plugin borracharia funcionando!"})
