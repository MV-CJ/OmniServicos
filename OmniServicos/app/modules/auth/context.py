from flask_jwt_extended import get_jwt, get_jwt_identity

def current_user():
    claims = get_jwt()

    return {
        "id": int(get_jwt_identity()),
        "empresa_id": claims["empresa_id"],
        "role": claims.get("role")
    }
