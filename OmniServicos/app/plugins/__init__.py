from .vidracaria.routes import vidracaria_bp

def register_plugins(app):
    app.register_blueprint(vidracaria_bp, url_prefix="/plugin/vidracaria")
