from flask import jsonify
from sqlalchemy import func
from flask_jwt_extended import jwt_required

from . import command_center_bp
from app.models import Produto
from app.extensions import db
from app.modules.auth.context import current_user


@command_center_bp.route("/metrics/products")
@jwt_required()
def product_metrics():
    empresa_id = current_user()["empresa_id"]

    total_produtos = db.session.query(func.count(Produto.id))\
        .filter(Produto.empresa_id == empresa_id)\
        .scalar()

    produtos_alerta = db.session.query(func.count(Produto.id))\
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.quantidade <= Produto.quantidade_minima,
            Produto.ativo.is_(True)
        ).scalar()

    produtos_zerados = db.session.query(func.count(Produto.id))\
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.quantidade == 0,
            Produto.ativo.is_(True)
        ).scalar()

    return jsonify({
        "total_produtos": total_produtos,
        "produtos_em_alerta": produtos_alerta,
        "produtos_zerados": produtos_zerados
    })


@command_center_bp.route("/alerts/low-stock")
@jwt_required()
def produtos_em_alerta():
    empresa_id = current_user()["empresa_id"]

    produtos = Produto.query.filter(
        Produto.empresa_id == empresa_id,
        Produto.quantidade <= Produto.quantidade_minima,
        Produto.ativo.is_(True)
    ).order_by(Produto.quantidade.asc()).all()

    return jsonify([
        {
            "id": p.id,
            "sku": p.cd_sku,
            "nome": p.nome,
            "quantidade": p.quantidade,
            "quantidade_minima": p.quantidade_minima
        }
        for p in produtos
    ])


@command_center_bp.route("/alerts/out-of-stock")
@jwt_required()
def produtos_zerados():
    empresa_id = current_user()["empresa_id"]

    produtos = Produto.query.filter(
        Produto.empresa_id == empresa_id,
        Produto.quantidade == 0,
        Produto.ativo.is_(True)
    ).order_by(Produto.nome).all()

    return jsonify([
        {
            "id": p.id,
            "sku": p.cd_sku,
            "nome": p.nome
        }
        for p in produtos
    ])


@command_center_bp.route("/metrics/top-products")
@jwt_required()
def top_products():
    empresa_id = current_user()["empresa_id"]

    mais_estoque = Produto.query.filter(
        Produto.empresa_id == empresa_id,
        Produto.ativo.is_(True)
    ).order_by(Produto.quantidade.desc()).limit(5).all()

    menos_estoque = Produto.query.filter(
        Produto.empresa_id == empresa_id,
        Produto.ativo.is_(True)
    ).order_by(Produto.quantidade.asc()).limit(5).all()

    return jsonify({
        "mais_estoque": [
            {"sku": p.cd_sku, "nome": p.nome, "quantidade": p.quantidade}
            for p in mais_estoque
        ],
        "menos_estoque": [
            {"sku": p.cd_sku, "nome": p.nome, "quantidade": p.quantidade}
            for p in menos_estoque
        ]
    })


@command_center_bp.route("/dashboard")
@jwt_required()
def dashboard():
    empresa_id = current_user()["empresa_id"]

    total_produtos = db.session.query(func.count(Produto.id))\
        .filter(Produto.empresa_id == empresa_id)\
        .scalar()

    produtos_alerta = db.session.query(func.count(Produto.id))\
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.quantidade <= Produto.quantidade_minima,
            Produto.ativo.is_(True)
        ).scalar()

    produtos_zerados = db.session.query(func.count(Produto.id))\
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.quantidade == 0,
            Produto.ativo.is_(True)
        ).scalar()

    return jsonify({
        "estoque": {
            "total_produtos": total_produtos,
            "produtos_em_alerta": produtos_alerta,
            "produtos_zerados": produtos_zerados
        },
        "status": "ok"
    })

