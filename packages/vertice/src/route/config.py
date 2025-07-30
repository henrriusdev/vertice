import traceback
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from src.service.configuracion import get_configuracion, add_configuracion, update_configuracion
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo

cfg = Blueprint('config_blueprint', __name__)

@cfg.route('/', methods=['GET'])
async def get_one_config():
    try:
        configuracion = await get_configuracion(1)
        if configuracion:
            return jsonify({"ok": True, "status": 200, "data": configuracion})
        return jsonify({"ok": False, "status": 204, "data": {"message": "config no disponible"}}), 204
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@cfg.route('/add', methods=['POST'])
@jwt_required()
async def add_config():
    try:
        usuario = await get_usuario_por_correo(get_jwt().get('sub'))
        payload = request.json

        await add_configuracion(payload)

        await add_trazabilidad({
            "accion": f"Añadir Configuración con ciclo: {payload['ciclo']}",
            "usuario": usuario,
            "modulo": "General",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@cfg.route('/update', methods=['PUT'])
@jwt_required()
async def update_config():
    try:
        usuario = await get_usuario_por_correo(get_jwt().get('sub'))
        payload = request.json

        await update_configuracion(payload)

        await add_trazabilidad({
            "accion": f"Actualizar Configuración",
            "usuario": usuario,
            "modulo": "General",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

