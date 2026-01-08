from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User, Empresa
from app.modules.auth.context import current_user
from app.modules.auth.decorators import roles_required
from app.modules.auth.roles import USER, MANAGER, ADMIN
from . import users_bp


@users_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data.get("email") or not data.get("password") or not data.get("empresa_nome"):
        return jsonify({"error": "Dados obrigatórios ausentes"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já cadastrado"}), 409

    # 1. cria empresa
    empresa = Empresa(
        nome=data["empresa_nome"],
        cnpj=data.get("cnpj")
    )
    db.session.add(empresa)
    db.session.flush()  # pega empresa.id

    # 2. cria usuário ADMIN
    user = User(
        empresa_id=empresa.id,
        name=data.get("name"),
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role=ADMIN
    )

    db.session.add(user)
    db.session.commit()

    # 3. gera token
    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "empresa_id": empresa.id,
            "role": user.role
        }
    )

    return jsonify({
        "message": "Empresa e usuário criados com sucesso",
        "access_token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "empresa_id": empresa.id,
            "role": user.role
        }
    }), 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(
        email=data.get("email"),
        ativo=True
    ).first()

    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "empresa_id": user.empresa_id,
            "role": user.role
        }
    )

    return jsonify({
        "access_token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "empresa_id": user.empresa_id,
            "role": user.role
        }
    }), 200

@users_bp.route("", methods=["POST"])
@roles_required(MANAGER, ADMIN)
def criar_usuario():
    user_ctx = current_user()
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já existe"}), 409

    user = User(
        empresa_id=user_ctx["empresa_id"],
        name=data.get("name"),
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role=data.get("role", USER)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Usuário criado com sucesso",
        "user_id": user.id
    }), 201


@users_bp.route("/<int:user_id>", methods=["PUT"])
@roles_required(ADMIN)
def atualizar_usuario(user_id):
    user_ctx = current_user()

    user = User.query.filter_by(
        id=user_id,
        empresa_id=user_ctx["empresa_id"]
    ).first_or_404()

    data = request.get_json()

    for campo in ["name", "role", "ativo"]:
        if campo in data:
            setattr(user, campo, data[campo])

    db.session.commit()
    return jsonify({"message": "Usuário atualizado com sucesso"})
