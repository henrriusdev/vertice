from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required

from src.service.coordinadores import (
    get_coordinadores,
    get_coordinador,
    add_coordinador,
    update_coordinador,
    delete_coordinador,
    toggle_coordinador_status
)
from src.service.estudiantes import get_notas_estudiante
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo

crd = Blueprint('coordinacion_blueprint', __name__)

@crd.route('/')
@jwt_required()
async def listar_coordinadores():
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    data = await get_coordinadores()
    await add_trazabilidad({"accion": "Obtener Coordinadores", "usuario": usuario, "modulo": "Coordinacion", "nivel_alerta": 1})
    return jsonify({"ok": True, "status": 200, "data": data})

@crd.route('/<cedula>')
@jwt_required()
async def obtener_coordinador(cedula):
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    data = await get_coordinador(cedula)
    if data:
        await add_trazabilidad({"accion": f"Obtener Coordinador {cedula}", "usuario": usuario, "modulo": "Coordinacion", "nivel_alerta": 1})
        return jsonify({"ok": True, "status": 200, "data": data})
    return jsonify({"ok": False, "status": 404, "data": {"message": "coordinador no encontrado"}}), 404

@crd.route('/add', methods=['POST'])
@jwt_required()
async def nuevo_coordinador():
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    payload = request.json
    await add_coordinador(payload["usuario_id"], payload["carrera_id"], payload["telefono"])
    await add_trazabilidad({"accion": f"Añadir Coordinador {payload['usuario_id']}", "usuario": usuario, "modulo": "Coordinacion", "nivel_alerta": 2})
    return jsonify({"ok": True, "status": 200})

@crd.route('/update/<int:id_coordinador>', methods=['PUT'])
@jwt_required()
async def actualizar_coordinador(id_coordinador):
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    payload = request.json
    await update_coordinador(id_coordinador, payload["carrera_id"], payload["telefono"])
    await add_trazabilidad({"accion": f"Actualizar Coordinador {id_coordinador}", "usuario": usuario, "modulo": "Coordinacion", "nivel_alerta": 2})
    return jsonify({"ok": True, "status": 200})

@crd.route('/delete/<cedula>', methods=['DELETE'])
@jwt_required()
async def eliminar_coordinador(cedula):
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    await delete_coordinador(cedula)
    await add_trazabilidad({"accion": f"Eliminar Coordinador {cedula}", "usuario": usuario, "modulo": "Coordinacion", "nivel_alerta": 3})
    return jsonify({"ok": True, "status": 200})

@crd.route('/toggle-status/<cedula>', methods=['PUT'])
@jwt_required()
async def toggle_status_coordinador(cedula):
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    result = await toggle_coordinador_status(cedula)
    if result:
        await add_trazabilidad({"accion": f"Cambiar Estado de Coordinador {cedula}", "usuario": usuario, "modulo": "Coordinacion", "nivel_alerta": 2})
        return jsonify({"ok": True, "status": 200})
    return jsonify({"ok": False, "status": 404, "data": {"message": "Coordinador no encontrado"}}), 404

@crd.route('/materias/<cedula>', methods=['GET'])
@jwt_required()
async def obtener_notas_estudiante(cedula):
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    data = await get_notas_estudiante(cedula)
    await add_trazabilidad({"accion": f"Obtener Notas del Estudiante {cedula}", "usuario": usuario, "modulo": "Estudiante", "nivel_alerta": 1})
    return jsonify({"ok": True, "status": 200, "data": data})
