import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://omni_user:omni_pass@localhost:5432/omni_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
