from . import erp_bp
from flask import jsonify

@erp_bp.route("/test")
def test_erp():
    return jsonify({"message": "ERP funcionando!"})
