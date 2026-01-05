import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://omni_user:omni_pass@localhost:5432/omni_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
