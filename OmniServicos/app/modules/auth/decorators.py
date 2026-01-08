from functools import wraps
from flask_jwt_extended import jwt_required
from flask import jsonify
from app.modules.auth.context import current_user

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = current_user()

            user_role = user["role"].lower()

            allowed_roles = [r.lower() for r in roles]

            if user_role not in allowed_roles:
                return jsonify({
                    "error": "Acesso não autorizado",
                    "required_roles": allowed_roles,
                    "user_role": user_role
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
