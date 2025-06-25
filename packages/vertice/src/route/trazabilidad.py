from datetime import datetime
from functools import wraps

from flask import Blueprint, jsonify, request

from src.model import Usuario
from src.service.trazabilidad import get_trazabilidad
from flask_jwt_extended import jwt_required, get_jwt

trz = Blueprint('trazabilidad_blueprint', __name__)

@trz.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def superuser_required():
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return jsonify({"ok": False, "status": 401, "data": {"message": "Token no proporcionado"}}), 401

            token = auth[7:]
            try:
                payload = get_jwt()
                email = payload.get("sub")
                if not email:
                    raise Exception("ID de usuario no presente en el token")
            except Exception as ex:
                return jsonify({"ok": False, "status": 401, "data": {"message": f"Token inválido: {str(ex)}"}}), 401

            try:
                usuario = await Usuario.get(correo=email).prefetch_related("rol")
            except Exception:
                return jsonify({"ok": False, "status": 401, "data": {"message": "Usuario no encontrado"}}), 401

            if usuario.rol.nombre.lower() != "administrador":
                return jsonify({"ok": False, "status": 403, "data": {"message": "Acceso denegado"}}), 403

            return await fn(*args, **kwargs)
        return wrapper
    return decorator


@trz.post('/')
@jwt_required()
@superuser_required()
async def list_trazabilidad():
    try:
        filtros = {
            "busqueda": request.json.get("busqueda", "").strip(),
            "fechaDesde": request.json.get("fechaDesde", "").strip(),
            "fechaHasta": request.json.get("fechaHasta", "").strip(),
            "rol": request.json.get("rol", "").strip()
        }

        if filtros["fechaDesde"]:
            filtros["fechaDesde"] = datetime.strptime(filtros["fechaDesde"], "%Y-%m-%d").date()
        if filtros["fechaHasta"]:
            filtros["fechaHasta"] = datetime.strptime(filtros["fechaHasta"], "%Y-%m-%d").date()

        data = await get_trazabilidad(filtros)
        return jsonify({"ok": True, "status": 200, "data": data})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500