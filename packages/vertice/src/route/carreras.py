from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from src.service.carrera import get_carreras, get_carrera, add_carrera, update_carrera, delete_carrera
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo

car = Blueprint("carrera_blueprint", __name__)


@car.route('/')
@jwt_required()
async def list_carreras():
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    await add_trazabilidad({"accion": "Obtener Carreras", "usuario": usuario, "modulo": "General", "nivel_alerta": 1})
    data = await get_carreras()
    return jsonify({"ok": True, "status": 200, "data": data})


@car.route('/<int:id>')
@jwt_required()
async def get_one_carrera(id):
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    await add_trazabilidad({"accion": f"Obtener Carrera {id}", "usuario": usuario, "modulo": "General", "nivel_alerta": 1})
    data = await get_carrera(id)
    return jsonify({"ok": True, "status": 200, "data": data})


@car.route('/add', methods=['POST'])
@jwt_required()
async def add_new():
    payload = request.json
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    await add_carrera(payload)
    await add_trazabilidad({"accion": f"Añadir Carrera {payload['id']}", "usuario": usuario, "modulo": "General", "nivel_alerta": 2})
    return jsonify({"ok": True, "status": 200})


@car.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
async def update_one(id: int):
    print(id)
    payload = request.json
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    await update_carrera(id, payload)
    await add_trazabilidad({"accion": f"Actualizar Carrera {id}", "usuario": usuario, "modulo": "General", "nivel_alerta": 2})
    return jsonify({"ok": True, "status": 200})


@car.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
async def delete_one(id):
    claims = get_jwt()
    await delete_carrera(id)
    await add_trazabilidad({"accion": f"Eliminar Carrera {id}", "usuario": await get_usuario_por_correo(claims.get('sub')), "modulo": "General", "nivel_alerta": 3})
    return jsonify({"ok": True, "status": 200})