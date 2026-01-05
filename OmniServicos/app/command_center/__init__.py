from flask import Blueprint

command_center_bp = Blueprint("command_center", __name__)

from . import routes
