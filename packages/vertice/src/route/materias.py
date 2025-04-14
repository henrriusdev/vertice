from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
import traceback

from src.service.usuarios import get_usuario_por_correo
from src.service.materias import (
    get_materias, get_materia, get_materias_validas,
    add_materia, modificar_materia_estudiante, update_materia, delete_materia
)
from src.service.trazabilidad import add_trazabilidad
from src.service.configuracion import get_configuracion

mat = Blueprint('materia_blueprint', __name__)

@mat.route('/')
@jwt_required()
async def listar_materias():
    usuario = await get_usuario_por_correo(get_jwt().get('sub'))
    await add_trazabilidad({"accion": "Obtener todas las Materias", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 1})
    data = await get_materias()
    return jsonify({"ok": True, "status": 200, "data": data})

@mat.route('/<id>')
@jwt_required()
async def obtener_materia(id: str):
    usuario = get_jwt().get('nombre')
    data = await get_materia(id)
    if data:
        await add_trazabilidad({"accion": f"Obtener Materia con id: {id}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 1})
        return jsonify({"ok": True, "status": 200, "data": data})
    return jsonify({"ok": False, "status": 404, "data": {"message": "materia no encontrada"}}), 404

@mat.route('/inscribir/<cedula_estudiante>', methods=['GET'])
@jwt_required()
async def materias_validas(cedula_estudiante: str):
    usuario = get_jwt().get('nombre')
    try:
        materias = await get_materias_validas(cedula_estudiante)
        if not materias:
            return jsonify({"ok": False, "status": 404, "data": {"message": "No se pueden inscribir materias"}}), 404
        await add_trazabilidad({"accion": f"Materias válidas para inscripción de {cedula_estudiante}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 1})
        return jsonify({"ok": True, "status": 200, "data": {"materias": materias}})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@mat.route('/add', methods=['POST'])
@jwt_required()
async def crear_materia():
    usuario = get_jwt().get('nombre')
    data = request.json
    config = await get_configuracion("1")
    data["ciclo"] = config["ciclo"]
    try:
        await add_materia(data)
        await add_trazabilidad({"accion": f"Añadir Materia {data['id']}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 2})
        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@mat.route('/update/<id>', methods=['PUT'])
@jwt_required()
async def modificar_materia(id):
    usuario = get_jwt().get('nombre')
    data = request.json
    data["id"] = id
    config = await get_configuracion("1")
    data["ciclo"] = config["ciclo"]
    try:
        await update_materia(id, data)
        await add_trazabilidad({"accion": f"Actualizar Materia {id}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 2})
        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@mat.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
async def eliminar_materia(id):
    usuario = get_jwt().get('nombre')
    try:
        await delete_materia(id)
        await add_trazabilidad({"accion": f"Eliminar Materia {id}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 3})
        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@mat.route("/upload", methods=["PATCH"])
@jwt_required()
async def modificar_materia_estudiante_route():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cedula_estudiante = request.json.get('cedula_estudiante')
        nombre_campo = request.json.get('nombre_campo')
        valor = request.json.get('valor')
        materia = request.json.get('materia')

        await modificar_materia_estudiante(materia, cedula_estudiante, nombre_campo, valor)

        await add_trazabilidad({
            "accion": f"Modificar nota del estudiante {cedula_estudiante}, campo: {nombre_campo}, valor: {valor}",
            "usuario": usuario,
            "modulo": "Materias",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200, "data": None}), 200
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
