from flask import request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from urllib.parse import urlencode
from app.extensions import db, oauth
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

    empresa = Empresa(
        nome=data["empresa_nome"],
        cnpj=data.get("cnpj")
    )
    db.session.add(empresa)
    db.session.flush()

    user = User(
        empresa_id=empresa.id,
        name=data.get("name"),
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role=ADMIN,
        ativo=True
    )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "empresa_id": empresa.id,
            "role": user.role
        }
    )

    return jsonify({
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

    if not user or not user.password:
        return jsonify({"error": "Credenciais inválidas"}), 401

    if not check_password_hash(user.password, data.get("password")):
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


@users_bp.route("/login/google")
def login_google():
    redirect_uri = url_for("users.login_google_callback", _external=True)
    return oauth.google.authorize_redirect(
        redirect_uri,
        prompt="select_account"
    )


@users_bp.route("/login/google/callback")
def login_google_callback():
    token = oauth.google.authorize_access_token()
    user_info = token.get("userinfo")

    if not user_info:
        return redirect("http://localhost:3000/login?error=google_auth")

    email = user_info["email"]
    name = user_info.get("name")
    google_id = user_info.get("sub") # ID único do Google
    picture = user_info.get("picture") # URL da imagem

    user = User.query.filter_by(email=email).first()

    if not user:
        # Primeiro login: cria empresa e usuário
        empresa = Empresa(nome=f"Empresa de {name}")
        db.session.add(empresa)
        db.session.flush()

        user = User(
            empresa_id=empresa.id,
            name=name,
            email=email,
            google_id=google_id,
            profile_pic=picture,
            password=None,
            role=USER,
            ativo=True
        )
        db.session.add(user)
    else:
        # Usuário já existe: atualizamos a foto e o ID do Google se necessário
        user.profile_pic = picture
        user.google_id = google_id

    db.session.commit()

    # IMPORTANTE: Coloque os dados extras no JWT para o Front ler imediatamente
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "empresa_id": user.empresa_id,
            "empresa_nome": user.empresa.nome, # Enviando o nome da empresa
            "role": user.role,
            "name": user.name,
            "picture": user.profile_pic # Enviando a foto para o Sidebar
        }
    )

    query = urlencode({"token": access_token})
    return redirect(f"http://localhost:3000/auth/callback?{query}")


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
        role=data.get("role", USER),
        ativo=True
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso", "user_id": user.id}), 201


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


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "picture": user.profile_pic,
        "empresa": {
            "id": user.empresa.id,
            "nome": user.empresa.nome,
            "cnpj": user.empresa.cnpj,
            "ativo": user.empresa.ativo
        }
    }), 200

@users_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # JWT é stateless → não há o que invalidar no servidor
    # Esta rota existe para padronizar o fluxo de logout
    return jsonify({"message": "Logout realizado com sucesso"}), 200
