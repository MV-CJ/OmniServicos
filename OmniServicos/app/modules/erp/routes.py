from . import erp_bp
from flask import jsonify
from flask import request
from app.models import Produto
from app.extensions import db 

#### Gerenciamento de produtos
@erp_bp.route("/list_products", methods=["GET"])
def listar_produtos():
    # --- Paginação ---
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)  # default 20 por página
    per_page = min(per_page, 100)  # limite máximo de 100 por request

    # --- Filtros ---
    busca = request.args.get("busca", type=str)        # busca por nome ou SKU
    categoria = request.args.get("categoria", type=str)

    query = Produto.query

    if busca:
        query = query.filter(
            (Produto.nome.ilike(f"%{busca}%")) |
            (Produto.cd_sku.ilike(f"%{busca}%"))
        )
    if categoria:
        query = query.filter_by(categoria=categoria)

    # --- Paginação ---
    paginated = query.order_by(Produto.nome).paginate(page=page, per_page=per_page, error_out=False)

    produtos = [p.to_dict() for p in paginated.items]

    return jsonify({
        "produtos": produtos,
        "total": paginated.total,
        "page": paginated.page,
        "per_page": paginated.per_page,
        "pages": paginated.pages
    })


# Criar produto
@erp_bp.route("/list_products", methods=["POST"])
def criar_produto():
    data = request.get_json()
    novo_produto = Produto(
        cd_sku=data.get("cd_sku"),
        cd_ean=data.get("cd_ean"),
        nome=data.get("nome"),
        descricao=data.get("descricao"),
        categoria=data.get("categoria"),
        vl_compra=data.get("vl_compra", 0.0),
        porcent_lucro=data.get("porcent_lucro", 0.0),
        vl_venda=data.get("vl_venda", 0.0),   # recebe do front
        quantidade=data.get("quantidade", 0),
        quantidade_minima= data.get("quantidade_minima",0),
        peso_kg=data.get("peso_kg", 0.0),
        largura_cm=data.get("largura_cm", 0.0),
        altura_cm=data.get("altura_cm", 0.0),
        profundidade_cm=data.get("profundidade_cm", 0.0),
        foto_url=data.get("foto_url"),
        ativo=data.get("ativo", True)
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify(novo_produto.to_dict()), 201


# Atualizar produto
@erp_bp.route("/list_products/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    data = request.get_json()
    for campo in ["cd_sku","cd_ean","nome","descricao","categoria",
                    "vl_compra","porcent_lucro","vl_venda","quantidade",
                    "peso_kg","largura_cm","altura_cm","profundidade_cm",
                    "foto_url","ativo"]:
        if campo in data:
            setattr(produto, campo, data[campo])
    db.session.commit()
    return jsonify(produto.to_dict())

# Deletar produto
@erp_bp.route("/list_products/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    db.session.delete(produto)
    db.session.commit()

    return jsonify({
        "message": "Produto removido com sucesso",
        "produto_id": produto_id
    }), 200
    

#### Gerenciamento do estoque 
