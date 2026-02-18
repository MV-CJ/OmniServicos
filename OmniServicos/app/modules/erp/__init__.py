from flask import Blueprint

erp_bp = Blueprint("erp", __name__)

from . import routes
