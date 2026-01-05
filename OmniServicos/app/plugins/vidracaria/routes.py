from flask import Blueprint, jsonify

vidracaria_bp = Blueprint("vidracaria", __name__)

@vidracaria_bp.route("/test")
def test_vidracaria():
    return jsonify({"message": "Plugin vidracaria funcionando!"})
