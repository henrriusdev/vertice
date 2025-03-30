from flask import Blueprint, request, jsonify, send_from_directory, send_file, render_template
from flask_jwt_extended import jwt_required, get_jwt
from os import getcwd, path, remove, makedirs
from datetime import datetime, date
from io import BytesIO
from weasyprint import HTML
import traceback

from src.service.trazabilidad import add_trazabilidad
from src.service.estudiantes import get_student, get_materias_inscritas
from src.service.carrera import get_carrera
from src.service.materias import listar_materias_asignadas

arc = Blueprint("archivo", __name__)
PATH_FILES = getcwd() + "/planificacion/"

def create_folder_if_not_exists(folder_path):
    if not path.exists(folder_path):
        makedirs(folder_path)


# ----------------------- ARCHIVOS -----------------------

@arc.post("/upload")
@jwt_required()
def upload_file():
    claims = get_jwt()
    usuario = claims.get('nombre')
    file = request.files['file']
    ciclo = request.form.get('ciclo', '')
    folder = request.form.get('folder', '')

    ciclo_path = path.join(PATH_FILES, ciclo)
    create_folder_if_not_exists(ciclo_path)

    folder_path = path.join(ciclo_path, folder)
    create_folder_if_not_exists(folder_path)

    file.save(path.join(folder_path, file.filename))

    # Trazabilidad
    add_trazabilidad({
        "accion": f"Subir archivo: {file.filename} a carpeta: {folder}, ciclo: {ciclo}",
        "usuario": usuario,
        "modulo": "Archivos",
        "nivel_alerta": 2
    })

    return jsonify({"ok": True, "status": 200})


@arc.get("/file/<string:name_file>")
@jwt_required()
def get_file(name_file):
    claims = get_jwt()
    usuario = claims.get('nombre')
    folder = request.args.get("folder", "")
    ciclo = request.args.get("ciclo", "")
    file_path = path.join(PATH_FILES + ciclo, folder, name_file)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 404, "data": {"message": "Archivo no encontrado"}}), 404

    # Trazabilidad
    add_trazabilidad({
        "accion": f"Obtener archivo: {name_file} del folder: {folder}, ciclo: {ciclo}",
        "usuario": usuario,
        "modulo": "Archivos",
        "nivel_alerta": 1
    })

    return send_from_directory(path.join(PATH_FILES, ciclo, folder), path=name_file, as_attachment=False)


@arc.get("/download/<string:name_file>")
@jwt_required()
def download_file(name_file):
    claims = get_jwt()
    usuario = claims.get('nombre')
    folder = request.args.get("folder", "")
    ciclo = request.args.get("ciclo", "")
    file_path = path.join(PATH_FILES + ciclo, folder, name_file)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 404, "data": {"message": "Archivo no encontrado"}}), 404

    # Trazabilidad
    add_trazabilidad({
        "accion": f"Descargar archivo: {name_file} de carpeta: {folder}, ciclo: {ciclo}",
        "usuario": usuario,
        "modulo": "Archivos",
        "nivel_alerta": 1
    })

    return send_from_directory(path.join(PATH_FILES, ciclo, folder), path=name_file, as_attachment=True)


@arc.delete('/delete')
@jwt_required()
def delete_file():
    claims = get_jwt()
    usuario = claims.get('nombre')
    filename = request.json.get('filename', '')
    folder = request.json.get('folder', '')
    ciclo = request.json.get('ciclo', '')

    file_path = path.join(PATH_FILES + ciclo, folder, filename)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 404, "data": {"message": "Archivo no encontrado"}}), 404

    try:
        remove(file_path)

        # Trazabilidad
        add_trazabilidad({
            "accion": f"Eliminar archivo: {filename} de carpeta: {folder}, ciclo: {ciclo}",
            "usuario": usuario,
            "modulo": "Archivos",
            "nivel_alerta": 3
        })

        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


# ----------------------- PDF -----------------------

@arc.get('/estudiante/<cedula>')
@jwt_required()
def generar_ficha_estudiantil(cedula):
    try:
        estudiante = get_student(cedula)
        if not estudiante:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404

        materias = get_materias_inscritas(cedula)
        carrera = get_carrera(estudiante["carrera"])

        estudiante["carrera"] = carrera["nombre"]
        fecha_actual = date.today().strftime("%d/%m/%Y")

        html = render_template("fichaEstudiantes.html", student=estudiante, materias=materias["contenido"], fecha_actual=fecha_actual)
        pdf = HTML(string=html).write_pdf()
        return send_file(BytesIO(pdf), download_name="ficha_estudiantil.pdf", as_attachment=True)
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@arc.get('/materias_asignadas')
@jwt_required()
def materias_asignadas():
    try:
        data = listar_materias_asignadas()
        if not data:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Datos no encontrados"}}), 404

        fecha_actual = date.today().strftime("%d/%m/%Y")
        html = render_template("docenteria.html", materias=data, fecha_actual=fecha_actual)
        pdf = HTML(string=html).write_pdf()
        return send_file(BytesIO(pdf), download_name="docentes_materias.pdf", as_attachment=True)
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
