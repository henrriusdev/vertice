from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from src.service.estudiantes import (
    get_students,
    get_student,
    add_student,
    update_student,
    delete_student,
    toggle_student_status,
    add_materia,
    get_notas_estudiante,
    get_historico,
    get_inscritas,
    validar_pagos_estudiante
)
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo
from src.service.coordinadores import get_coordinador_by_usuario

est = Blueprint('students_blueprint', __name__)

@est.route('/')
@jwt_required()
async def list_students():
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
        "accion": "Obtener todos los estudiantes",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    data = await get_students(carrera_id=carrera_id)
    return jsonify({"ok": True, "status": 200, "data": data})


@est.route("/materias", methods=["GET"])
@jwt_required()
async def listar_notas():
    correo = get_jwt_identity()
    claims = get_jwt()

    await validar_pagos_estudiante(correo)

    estudiante = await get_usuario_por_correo(correo)
    data = await get_notas_estudiante(estudiante.cedula)

    await add_trazabilidad({
        "accion": f"Obtener notas del estudiante con cédula: {estudiante.cedula}",
        "usuario": estudiante,
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": data})


@est.route("/historico", methods=["GET"])
@jwt_required()
async def listar_historico():
    correo = get_jwt_identity()
    claims = get_jwt()

    estudiante = await get_usuario_por_correo(correo)
    data = await get_historico(estudiante.cedula)

    await add_trazabilidad({
        "accion": f"Obtener histórico del estudiante con cédula: {estudiante.cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": data})


@est.route("/horario", methods=["GET"])
@jwt_required()
async def listar_horario():
    correo = get_jwt_identity()
    claims = get_jwt()

    estudiante = await get_usuario_por_correo(correo)
    data = await get_inscritas(estudiante.cedula)

    await add_trazabilidad({
        "accion": f"Obtener horario del estudiante con cédula: {estudiante.cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": {"materias": data}})


@est.route("/horario/<cedula>", methods=["GET"])
@jwt_required()
async def listar_horario_por_cedula(cedula):
    claims = get_jwt()
    data = await get_inscritas(cedula)

    await add_trazabilidad({
        "accion": f"Obtener horario del estudiante con cédula: {cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": {"materias": data}})


@est.route("/historico/<cedula>", methods=["GET"])
@jwt_required()
async def listar_historico_por_cedula(cedula):
    claims = get_jwt()
    data = await get_historico(cedula)

    await add_trazabilidad({
        "accion": f"Obtener histórico del estudiante con cédula: {cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": {"notas": data}})



@est.route('/<cedula>')
@jwt_required()
async def one_student(cedula):
    claims = get_jwt()
    usuario = claims.get('nombre')
    data = await get_student(cedula)
    if not data:
        return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404
    await add_trazabilidad({
        "accion": f"Obtener estudiante con cédula: {cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": data})


@est.route('/add', methods=["POST"])
@jwt_required()
async def create_student():
    body = request.json
    claims = get_jwt()

    usuario = await add_student(body)
    await add_trazabilidad({
        "accion": f"Añadir estudiante con cédula: {usuario.cedula}, nombre: {usuario.nombre}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})


@est.route('/update/<int:id_estudiante>', methods=["PUT"])
@jwt_required()
async def patch_student(id_estudiante):
    body = request.json
    claims = get_jwt()
    usuario = claims.get("nombre")

    await update_student(id_estudiante, body)
    await add_trazabilidad({
        "accion": f"Actualizar estudiante {usuario}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})


@est.route('/delete/<cedula>', methods=["DELETE"])
@jwt_required()
async def remove_student(cedula):
    claims = get_jwt()
    eliminado = await delete_student(cedula)
    if not eliminado:
        return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404
    await add_trazabilidad({
        "accion": f"Eliminar estudiante con cédula: {cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 3
    })
    return jsonify({"ok": True, "status": 200})


@est.route('/toggle-status/<cedula>', methods=["PUT"])
@jwt_required()
async def toggle_status(cedula):
    claims = get_jwt()
    new_status = await toggle_student_status(cedula)
    
    status_text = "activado" if new_status else "inactivado"
    await add_trazabilidad({
        "accion": f"Estudiante con cédula: {cedula} {status_text}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200, "data": {"activo": new_status}})


@est.route("/add-materia", methods=["POST"])
@jwt_required()
async def inscribir_materia():
    correo = get_jwt_identity()
    claims = get_jwt()
    
    # Now expecting asignacion IDs instead of materia IDs
    asignaciones = request.json.get("asignaciones", request.json.get("materias", []))
    
    # Convert to integers since asignacion IDs are integers
    asignaciones = [int(id_asig) for id_asig in asignaciones]

    estudiante = await get_usuario_por_correo(correo)
    await add_materia(estudiante.cedula, asignaciones)

    await add_trazabilidad({
        "accion": f"Añadir secciones {asignaciones} al estudiante con cédula: {estudiante.cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})

@est.route('/notas/<cedula>', methods=['GET'])
@jwt_required()
async def obtener_notas_estudiante_route(cedula):
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    data = await get_notas_estudiante(cedula)
    await add_trazabilidad({"accion": f"Obtener Notas del Estudiante {cedula}", "usuario": usuario, "modulo": "Estudiante", "nivel_alerta": 1})
    return jsonify({"ok": True, "status": 200, "data": data})
