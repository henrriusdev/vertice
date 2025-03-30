from functools import wraps
from flask import current_app, jsonify
from flask_jwt_extended import get_jwt

from src.service.sesiones import verificar_sesion_activa

def unica_sesion_requerida(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        jti = get_jwt().get("jti")
        if not await verificar_sesion_activa(jti):
            return jsonify({"ok": False, "status": 401, "message": "Esta sesión ha sido cerrada"}), 401
        return await fn(*args, **kwargs)
    return wrapper