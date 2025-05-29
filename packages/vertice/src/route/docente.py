import traceback

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from src.service.docentes import (
    get_docentes,
    get_docente,
    get_peticiones_por_docente,
    add_docente,
    obtener_materias_por_email_docente,
    update_docente,
    delete_docente,
)
from src.service.materias import modificar_materia_estudiante
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo

doc = Blueprint('docentes_blueprint', __name__)

@doc.route('/')
@jwt_required()
async def get_all_docentes():
    claims = get_jwt()
    await add_trazabilidad({
        "accion": "Obtener Docentes",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
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
        "usuario": await get_usuario_por_correo(claims.get('sub')),
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
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Docentes",
        "nivel_alerta": 1
    })
    return jsonify({"ok": True, "status": 200, "data": data})


@doc.route('/add', methods=["POST"])
@jwt_required()
async def add_new_docente():
    claims = get_jwt()
    payload = request.json
    await add_docente(**payload)

    await add_trazabilidad({
        "accion": f"Añadir Docente con cédula: {payload['usuario_id']}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
        "modulo": "Docentes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})


@doc.route('/update/<int:id_docente>', methods=["PUT"])
@jwt_required()
async def update_one_docente(id_docente: int):
    claims = get_jwt()
    payload = request.json
    await update_docente(id_docente, **payload)

    await add_trazabilidad({
        "accion": f"Actualizar Docente con ID: {id_docente}",
        "usuario": await get_usuario_por_correo(claims.get('sub')),
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
        "usuario": await get_usuario_por_correo(claims.get('sub')),
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
        cedula_estudiante=body.get("cedula_estudiante"),
        nombre_campo=body.get("nombre_campo"),
        valor=body.get("valor")
    )

    await add_trazabilidad({
        "accion": f"Modificar nota del estudiante {body.get('cedula_estudiante')}, campo {body.get('nombre_campo')}",
        "usuario": get_jwt().get("nombre"),
        "modulo": "Docentes",
        "nivel_alerta": 2
    })
    return jsonify({"ok": True, "status": 200})


@doc.route("/materias", methods=["GET"])
@jwt_required()
async def materias_por_docente():
    try:
        email = get_jwt().get('sub')
        materias = await obtener_materias_por_email_docente(email)
        return jsonify({"data": materias, "ok": True, "status": 200}), 200
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}), 500