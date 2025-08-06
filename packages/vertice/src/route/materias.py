import traceback

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from src.service.materias import (
    get_materias, get_materia, get_materias_validas,
    add_materia, modificar_materia_estudiante, update_materia, delete_materia, Materia
)
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo
from src.service.coordinadores import get_coordinador_by_usuario


mat = Blueprint('materia_blueprint', __name__)

@mat.route('/')
@jwt_required()
async def get_all_materias():
    claims = get_jwt()
    correo = claims.get('sub')
    rol = claims.get('rol')
    carrera_id = None
    if rol == 'coordinador' and correo is not None:
        usuario = await get_usuario_por_correo(correo)
        if usuario:
            coordinador = await get_coordinador_by_usuario(usuario.id)
            if coordinador:
                carrera_id = coordinador.carrera_id
    await add_trazabilidad({
        "accion": "Obtener Materias",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Materias",
        "nivel_alerta": 1
    })
    data = await get_materias(carrera_id=carrera_id)
    return jsonify({"ok": True, "status": 200, "data": data})


@mat.route('/<id>')
@jwt_required()
async def obtener_materia(id: str):
    usuario = await get_usuario_por_correo(get_jwt().get('sub'))
    data = await get_materia(id)
    if data:
        await add_trazabilidad({"accion": f"Obtener Materia con id: {id}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 1})
        return jsonify({"ok": True, "status": 200, "data": data})
    return jsonify({"ok": False, "status": 404, "data": {"message": "materia no encontrada"}}), 404


@mat.route('/inscribir/<cedula_estudiante>', methods=['GET'])
@jwt_required()
async def materias_validas(cedula_estudiante: str):
    usuario = await get_usuario_por_correo(get_jwt().get('sub'))
    try:
        materias = await get_materias_validas(cedula_estudiante)
        if not materias:
            return jsonify({"ok": False, "status": 401, "data": {"message": "No se pueden inscribir materias"}}), 401
        await add_trazabilidad({"accion": f"Materias válidas para inscripción de {cedula_estudiante}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 1})
        return jsonify({"ok": True, "status": 200, "data": materias})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 204


@mat.route('/add', methods=['POST'])
@jwt_required()
async def crear_materia():
    usuario = await get_usuario_por_correo(get_jwt().get('sub'))
    data = request.json
    try:
        await add_materia(data)
        await add_trazabilidad({"accion": f"Añadir Materia {data['id']}", "usuario": usuario, "modulo": "Materias", "nivel_alerta": 2})
        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@mat.route('/update/<id_materia>', methods=['PUT'])
@jwt_required()
async def modificar_materia(id_materia: str):
    usuario = await get_usuario_por_correo(get_jwt().get('sub'))
    data = request.json
    data["id"] = id_materia
    try:
        await update_materia(data)
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
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@mat.route('/toggle-status/<id>', methods=['PUT'])
@jwt_required()
async def toggle_materia_status(id):
    usuario = await get_usuario_por_correo(get_jwt().get('sub'))
    try:
        materia = await get_materia(id)
        if not materia:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Materia no encontrada"}}), 404
            
        # Toggle the activo status
        await Materia.filter(id=id).update(activo=not materia["materia"]["activo"])
        
        await add_trazabilidad({
            "accion": f"Cambiar estado de materia {id}",
            "usuario": usuario,
            "modulo": "Materias",
            "nivel_alerta": 2
        })
        
        return jsonify({"ok": True, "status": 200, "data": {"activo": not materia["materia"]["activo"]}})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@mat.route("/upload", methods=["PATCH"])
@jwt_required()
async def modificar_materia_estudiante_route():
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))

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
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
