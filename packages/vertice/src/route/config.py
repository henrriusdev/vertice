from flask import Blueprint, jsonify, request
from src.service.configuracion import get_configuracion, add_configuracion, update_configuracion
from src.service.trazabilidad import add_trazabilidad
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

cfg = Blueprint('config_blueprint', __name__)

@cfg.route('/<id>')
async def get_one_config(id):
    try:
        configuracion = await get_configuracion(id)
        if configuracion:
            return jsonify({"ok": True, "status": 200, "data": configuracion})
        return jsonify({"ok": False, "status": 404, "data": {"message": "config no disponible"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@cfg.route('/add', methods=['POST'])
@jwt_required()
async def add_config():
    try:
        usuario = get_jwt().get('nombre')
        payload = request.json

        await add_configuracion(payload)

        await add_trazabilidad({
            "accion": f"Añadir Configuración con ciclo: {payload['ciclo']}",
            "usuario": usuario,
            "fecha": datetime.now(),
            "modulo": "General",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@cfg.route('/update/<id>', methods=['PUT'])
@jwt_required()
async def update_config(id):
    try:
        usuario = get_jwt().get('nombre')
        payload = request.json

        await update_configuracion(id, payload)

        await add_trazabilidad({
            "accion": f"Actualizar Configuración {id}",
            "usuario": usuario,
            "fecha": datetime.now(),
            "modulo": "General",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

