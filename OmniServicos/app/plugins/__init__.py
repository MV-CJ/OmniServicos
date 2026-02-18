from .vidracaria.routes import vidracaria_bp
from .cozinha.routes import cozinha_bp
from .borracharia.routes import borracharia_bp

def register_plugins(app):
    app.register_blueprint(vidracaria_bp, url_prefix="/plugin/vidracaria")
    app.register_blueprint(cozinha_bp, url_prefix="/plugin/cozinha")
    app.register_blueprint(borracharia_bp, url_prefix="/plugin/borracharia")