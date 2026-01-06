from . import command_center_bp
from flask import jsonify
from app.models import Produto
from app.extensions import db 

@command_center_bp.route("/dashboard")
def dashboard():
    total_produtos = Produto.query.count()  # Conta quantos produtos existem no banco
    return jsonify({
        "message": "Dashboard funcionando!",
        "total_produtos": total_produtos
    })
