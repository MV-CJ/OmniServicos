from . import command_center_bp
from flask import jsonify

@command_center_bp.route("/dashboard")
def dashboard():
    return jsonify({"message": "Dashboard funcionando!"})
