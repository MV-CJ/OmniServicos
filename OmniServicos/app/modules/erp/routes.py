from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.modules.auth.context import current_user
from app.modules.auth.decorators import roles_required
from app.modules.auth.roles import MANAGER, ADMIN
from app.models import Produto
from app.extensions import db
from . import erp_bp


@erp_bp.route("/products", methods=["GET"])
@jwt_required()
def listar_produtos():
    user = current_user()
    empresa_id = user["empresa_id"]

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    query = Produto.query.filter_by(empresa_id=empresa_id)

    paginated = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        "produtos": [p.to_dict() for p in paginated.items],
        "total": paginated.total
    })



from sqlalchemy import and_
from app.modules.auth.context import current_user

@erp_bp.route("/products", methods=["POST"])
@roles_required(MANAGER, ADMIN)
def criar_produto():
    data = request.get_json()
    user = current_user()

    empresa_id = user["empresa_id"]
    cd_sku = data.get("cd_sku")

    if not cd_sku:
        return jsonify({"error": "cd_sku é obrigatório"}), 400

    # 🔎 valida duplicidade SOMENTE dentro da empresa do JWT
    sku_existe = Produto.query.filter(
        Produto.empresa_id == empresa_id,
        Produto.cd_sku == cd_sku
    ).first()

    if sku_existe:
        return jsonify({
            "error": "SKU já cadastrado para esta empresa",
            "cd_sku": cd_sku
        }), 409

    produto = Produto(
        empresa_id=empresa_id,
        criado_por=user["id"],
        cd_sku=cd_sku,
        cd_ean=data.get("cd_ean"),
        nome=data.get("nome"),
        descricao=data.get("descricao"),
        categoria=data.get("categoria"),
        vl_compra=data.get("vl_compra", 0.0),
        porcent_lucro=data.get("porcent_lucro", 0.0),
        vl_venda=data.get("vl_venda", 0.0),
        quantidade=data.get("quantidade", 0),
        quantidade_minima=data.get("quantidade_minima", 0),
        quantidade_alerta=data.get("quantidade_alerta", 0),
        peso_kg=data.get("peso_kg", 0.0),
        largura_cm=data.get("largura_cm", 0.0),
        altura_cm=data.get("altura_cm", 0.0),
        profundidade_cm=data.get("profundidade_cm", 0.0),
        foto_url=data.get("foto_url"),
        ativo=data.get("ativo", True)
    )

    try:
        db.session.add(produto)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro ao salvar produto"}), 500

    return jsonify(produto.to_dict()), 201



@erp_bp.route("/products/<int:produto_id>", methods=["PUT"])
@roles_required(MANAGER, ADMIN)
def atualizar_produto(produto_id):
    produto = Produto.query.filter_by(
        id=produto_id,
        empresa_id=g.current_user.empresa_id
    ).first_or_404()

    data = request.get_json()

    campos_permitidos = [
        "cd_sku", "cd_ean", "nome", "descricao", "categoria",
        "vl_compra", "porcent_lucro", "vl_venda",
        "quantidade", "quantidade_minima", "quantidade_alerta",
        "peso_kg", "largura_cm", "altura_cm", "profundidade_cm",
        "foto_url", "ativo"
    ]

    for campo in campos_permitidos:
        if campo in data:
            setattr(produto, campo, data[campo])

    db.session.commit()
    return jsonify(produto.to_dict())


@erp_bp.route("/products/<int:produto_id>", methods=["DELETE"])
@roles_required(MANAGER, ADMIN)
def deletar_produto(produto_id):
    produto = Produto.query.filter_by(
        id=produto_id,
        empresa_id=g.current_user.empresa_id
    ).first_or_404()

    db.session.delete(produto)
    db.session.commit()

    return jsonify({
        "message": "Produto removido com sucesso",
        "produto_id": produto_id
    }), 200
