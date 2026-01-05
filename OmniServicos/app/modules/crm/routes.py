from . import crm_bp
from flask import jsonify

@crm_bp.route("/test")
def test_crm():
    return jsonify({"message": "CRM funcionando!"})
