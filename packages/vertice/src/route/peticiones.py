import traceback

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from src.service.peticiones import (
    get_peticiones,
    get_peticion,
    get_peticiones_pendientes,
    add_peticion,
    update_peticion,
    delete_peticion
)
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo

ptc = Blueprint('peticion_blueprint', __name__)


@ptc.route('/')
@jwt_required()
async def get_all_peticiones():
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))
        data = await get_peticiones()
        await add_trazabilidad({
            "accion": "Obtener todas las Peticiones",
            "usuario": usuario,
            "modulo": "Peticiones",
            "nivel_alerta": 1
        })
        return jsonify({"ok": True, "status": 200, "data": data})
    except Exception:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "error": "Error al obtener las peticiones"}), 500


@ptc.route('/<id>')
@jwt_required()
async def get_one_peticion(id):
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))
        data = await get_peticion(id)
        if not data:
            return jsonify({"ok": False, "status": 404, "data": {"message": "peticion no disponible"}}), 404
        await add_trazabilidad({
            "accion": f"Obtener Petición con id: {id}",
            "usuario": usuario,
            "modulo": "Peticiones",
            "nivel_alerta": 1
        })
        return jsonify({"ok": True, "status": 200, "data": data})
    except Exception:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "error": "Error al obtener la petición"}), 500


@ptc.route('/pendientes')
@jwt_required()
async def get_pending_peticiones():
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))
        data = await get_peticiones_pendientes()
        await add_trazabilidad({
            "accion": "Obtener todas las Peticiones Pendientes",
            "usuario": usuario,
            "modulo": "Peticiones",
            "nivel_alerta": 1
        })
        return jsonify({"ok": True, "status": 200, "data": data})
    except Exception:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "error": "Error al obtener peticiones pendientes"}), 500


@ptc.route('/add', methods=["POST"])
@jwt_required()
async def create_peticion():
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))
        body = request.json

        if body["estado"] not in ["Aprobado", "Denegado", "Pendiente"]:
            return jsonify({"error": "Valor inválido para el campo estado"}), 400

        await add_peticion(body)

        await add_trazabilidad({
            "accion": f"Añadir Petición para el estudiante con cédula: {body['id_estudiante']}, materia: {body['id_materia']}",
            "usuario": usuario,
            "modulo": "Peticiones",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200})
    except Exception:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "error": "Error al crear la petición"}), 500


@ptc.route('/update/<id>', methods=["PATCH"])
@jwt_required()
async def patch_peticion(id):
    try:
        data = request.json
        allowed_fields = ["id_docente", "descripcion", "estado", "id_estudiante", "id_materia", "campo"]
        fields = {k: v for k, v in data.items() if k in allowed_fields}
        if not fields:
            return jsonify({"error": "No se proporcionaron campos válidos para actualizar"}), 400

        fields["id"] = id
        await update_peticion(fields)
        return jsonify({"ok": True, "status": 200})
    except Exception:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "error": "Error al actualizar la petición"}), 500


@ptc.route('/delete/<id>', methods=["DELETE"])
@jwt_required()
async def remove_peticion(id):
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))
        result = await delete_peticion(id)

        if result:
            await add_trazabilidad({
                "accion": f"Eliminar Petición con id: {id}",
                "usuario": usuario,
                "modulo": "Peticiones",
                "nivel_alerta": 3
            })
            return jsonify({"ok": True, "status": 200})
        return jsonify({"ok": False, "status": 404, "data": {"message": "peticion no encontrada"}}), 404
    except Exception:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "error": "Error al eliminar la petición"}), 500
