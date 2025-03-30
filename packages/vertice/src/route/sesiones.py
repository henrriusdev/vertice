from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.service.sesiones import (
    obtener_sesiones_usuario,
    eliminar_sesion,
    eliminar_sesiones_usuario,
)

ses = Blueprint("sesiones_bp", __name__)

@ses.get("/")
@jwt_required()
async def listar_sesiones():
    correo = get_jwt_identity()
    sesiones = await obtener_sesiones_usuario(correo)
    data = [{"id": s.id, "jti": s.jti, "creado_en": s.creado_en.isoformat()} for s in sesiones]
    return jsonify({"ok": True, "status": 200, "data": data})


@ses.delete("/sesiones")
@jwt_required()
async def cerrar_esta_sesion():
    jti = get_jwt().get("jti")
    await eliminar_sesion(jti)
    return jsonify({"ok": True, "status": 200, "message": "Sesión actual cerrada"})


@ses.delete("/sesiones/all")
@jwt_required()
async def cerrar_todas_sesiones():
    correo = get_jwt_identity()
    await eliminar_sesiones_usuario(correo)
    return jsonify({"ok": True, "status": 200, "message": "Todas las sesiones han sido cerradas"})
