from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from src.service.estudiantes import (
    get_students,
    get_student,
    add_student,
    update_student,
    delete_student,
    add_materia,
    get_notas_estudiante,
    get_historico,
    get_inscritas,
    validar_pagos_estudiante
)
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo

est = Blueprint('students_blueprint', __name__)

@est.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@est.route('/')
@jwt_required()
async def list_students():
    claims = get_jwt()
    data = await get_students()
    await add_trazabilidad({
        "accion": "Obtener todos los estudiantes",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
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
    usuario = claims.get("nombre")

    estudiante = await get_usuario_por_correo(correo)
    data = await get_inscritas(estudiante.cedula)

    await add_trazabilidad({
        "accion": f"Obtener horario del estudiante con cédula: {estudiante.cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": {"materias": data}})


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
    usuario = claims.get("nombre")
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

@est.route("/add-materia/<materia>", methods=["POST"])
@jwt_required()
async def inscribir_materia(materia: str):
    correo = get_jwt_identity()
    claims = get_jwt()

    estudiante = await get_usuario_por_correo(correo)
    await add_materia(estudiante["cedula"], materia)

    await add_trazabilidad({
        "accion": f"Añadir materia {materia} al estudiante con cédula: {estudiante.cedula}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Estudiantes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})

