from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .extensions import db, migrate
from .modules.crm import crm_bp
from .modules.erp import erp_bp
from .modules.pdv import pdv_bp
from .modules.users import users_bp
from .command_center import command_center_bp
from .plugins import register_plugins

from app.extensions import oauth

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # JWT
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60 * 60 * 8  # 8h

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
    )

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # Blueprints principais
    app.register_blueprint(command_center_bp, url_prefix="/")
    app.register_blueprint(crm_bp, url_prefix="/crm")
    app.register_blueprint(erp_bp, url_prefix="/erp")
    app.register_blueprint(pdv_bp, url_prefix="/pdv")
    app.register_blueprint(users_bp, url_prefix="/users")

    # Plugins
    register_plugins(app)

    return app
