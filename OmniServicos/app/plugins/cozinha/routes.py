from flask import Blueprint, jsonify

cozinha_bp = Blueprint("cozinha", __name__)

@cozinha_bp.route("/test")
def test_cozinha():
    return jsonify({"message": "Plugin cozinha funcionando!"})
