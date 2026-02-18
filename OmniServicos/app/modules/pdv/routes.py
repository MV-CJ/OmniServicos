from . import pdv_bp
from flask import jsonify

@pdv_bp.route("/test")
def test_erp():
    return jsonify({"message": "PDV funcionando!"})
