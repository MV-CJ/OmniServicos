from flask import Blueprint

pdv_bp = Blueprint("pdv", __name__)

from . import routes
