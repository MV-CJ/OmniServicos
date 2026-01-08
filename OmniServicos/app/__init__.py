from flask import Flask
from .extensions import db, migrate
from .modules.crm import crm_bp
from .modules.erp import erp_bp
from .modules.pdv import pdv_bp
from .modules.users import users_bp
from .command_center import command_center_bp
from flask_jwt_extended import JWTManager
from .plugins import register_plugins

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # depois joga no .env
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60 * 60 * 8  # 8h

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Blueprints dos módulos
    app.register_blueprint(command_center_bp, url_prefix='/')
    app.register_blueprint(crm_bp, url_prefix="/crm")
    app.register_blueprint(erp_bp, url_prefix="/erp")
    app.register_blueprint(pdv_bp, url_prefix="/pdv")
    app.register_blueprint(users_bp, url_prefix="/users")
    

    # Blueprints dos plugins
    register_plugins(app)

    return app
