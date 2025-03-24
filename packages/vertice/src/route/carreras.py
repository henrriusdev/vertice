from flask import Blueprint, jsonify, request
from service.carrera import get_carreras, get_carrera, add_carrera, update_carrera, delete_carrera
from service.trazabilidad import add_trazabilidad
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

carrera = Blueprint("carrera_blueprint", __name__)

@carrera.route('/')
@jwt_required()
async def list_carreras():
    claims = get_jwt()
    await add_trazabilidad({"accion": "Obtener Carreras", "usuario": claims.get('nombre'), "modulo": "General", "nivel_alerta": 1})
    data = await get_carreras()
    return jsonify({"ok": True, "status": 200, "data": data})

@carrera.route('/<int:id>')
@jwt_required()
async def get_one_carrera(id):
    claims = get_jwt()
    await add_trazabilidad({"accion": f"Obtener Carrera {id}", "usuario": claims.get('nombre'), "modulo": "General", "nivel_alerta": 1})
    data = await get_carrera(id)
    return jsonify({"ok": True, "status": 200, "data": data})

@carrera.route('/add', methods=['POST'])
@jwt_required()
async def add_new():
    payload = request.json
    claims = get_jwt()
    await add_carrera(payload)
    await add_trazabilidad({"accion": f"Añadir Carrera {payload['id']}", "usuario": claims.get('nombre'), "modulo": "General", "nivel_alerta": 2})
    return jsonify({"ok": True, "status": 200})

@carrera.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
async def update_one(id: int):
    payload = request.json
    claims = get_jwt()
    await update_carrera(id, payload)
    await add_trazabilidad({"accion": f"Actualizar Carrera {id}", "usuario": claims.get('nombre'), "modulo": "General", "nivel_alerta": 2})
    return jsonify({"ok": True, "status": 200})

@carrera.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
async def delete_one(id):
    claims = get_jwt()
    await delete_carrera(id)
    await add_trazabilidad({"accion": f"Eliminar Carrera {id}", "usuario": claims.get('nombre'), "modulo": "General", "nivel_alerta": 3})
    return jsonify({"ok": True, "status": 200})