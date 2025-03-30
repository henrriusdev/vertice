from flask import Blueprint, jsonify, request
from src.service.docentes import (
    get_docentes,
    get_docente,
    get_peticiones_por_docente,
    add_docente,
    update_docente,
    delete_docente,
)
from src.service.trazabilidad import add_trazabilidad
from src.service.materias import modificar_materia_estudiante
from flask_jwt_extended import jwt_required, get_jwt

from datetime import datetime

doc = Blueprint('docentes_blueprint', __name__)

@doc.route('/')
@jwt_required()
async def get_all_docentes():
    claims = get_jwt()
    await add_trazabilidad({
        "accion": "Obtener Docentes",
        "usuario": claims.get('nombre'),
        "modulo": "Docentes",
        "nivel_alerta": 1
    })
    data = await get_docentes()
    return jsonify({"ok": True, "status": 200, "data": data})


@doc.route('/<cedula>')
@jwt_required()
async def get_one_docente(cedula: str):
    claims = get_jwt()
    docente = await get_docente(cedula)
    if not docente:
        return jsonify({"ok": False, "status": 404, "data": {"message": "docente no encontrado"}}), 404

    await add_trazabilidad({
        "accion": f"Obtener Docente con cédula: {cedula}",
        "usuario": claims.get('nombre'),
        "modulo": "Docentes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": docente})


@doc.route('/peticiones/<cedula>')
@jwt_required()
async def get_peticiones(cedula: str):
    claims = get_jwt()
    data = await get_peticiones_por_docente(cedula)

    await add_trazabilidad({
        "accion": f"Obtener Peticiones del Docente con cédula: {cedula}",
        "usuario": claims.get('nombre'),
        "modulo": "Docentes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": data})


@doc.route('/add', methods=["POST"])
@jwt_required()
async def add_new_docente():
    claims = get_jwt()
    payload = request.json
    await add_docente(payload)

    await add_trazabilidad({
        "accion": f"Añadir Docente con cédula: {payload['usuario']}",
        "usuario": claims.get('nombre'),
        "modulo": "Docentes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})


@doc.route('/update/<cedula>', methods=["PUT"])
@jwt_required()
async def update_one_docente(cedula: str):
    claims = get_jwt()
    payload = request.json
    await update_docente(cedula, payload)

    await add_trazabilidad({
        "accion": f"Actualizar Docente con cédula: {cedula}",
        "usuario": claims.get('nombre'),
        "modulo": "Docentes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})


@doc.route('/delete/<cedula>', methods=["DELETE"])
@jwt_required()
async def delete_one_docente(cedula: str):
    claims = get_jwt()
    await delete_docente(cedula)

    await add_trazabilidad({
        "accion": f"Eliminar Docente con cédula: {cedula}",
        "usuario": claims.get('nombre'),
        "modulo": "Docentes",
        "nivel_alerta": 3
    })
    return jsonify({"ok": True, "status": 200})


@doc.route("/upload", methods=["PATCH"])
@jwt_required()
async def actualizar_nota_estudiante():
    body = request.json
    await modificar_materia_estudiante(
        cod_materia=body.get("materia"),
        id_estudiante=body.get("cedula_estudiante"),
        campo=body.get("nombre_campo"),
        valor=body.get("valor")
    )

    await add_trazabilidad({
        "accion": f"Modificar nota del estudiante {body.get('cedula_estudiante')}, campo {body.get('nombre_campo')}",
        "usuario": get_jwt().get("nombre"),
        "modulo": "Docentes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})
