from flask import Blueprint, request, send_from_directory, jsonify
from os import getcwd, path, remove, makedirs
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from models.trazabilidadmodel import TrazabilidadModel
from models.entities.trazabilidad import Trazabilidad

files = Blueprint("files", __name__)

PATH_FILES = getcwd() + "/planificacion/"


def create_folder_if_not_exists(folder_path):
    if not path.exists(folder_path):
        makedirs(folder_path)


@files.post("/upload")
@jwt_required()
def upload_file():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        file = request.files['file']
        ciclo = request.form.get('ciclo', '')
        folder = request.form.get('folder', '')

        print(ciclo)
        print(file)
        ciclo_path = path.join(PATH_FILES, ciclo)
        create_folder_if_not_exists(ciclo_path)

        folder_path = path.join(ciclo_path, folder)
        create_folder_if_not_exists(folder_path)

        file.save(path.join(folder_path, file.filename))

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion=f"Subir archivo: {file.filename} a la carpeta: {folder} y ciclo: {ciclo}",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Archivos",
            nivel_alerta=2
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": None})
    except FileNotFoundError:
        return jsonify({"ok": False, "status": 500, "data": {"message": "Folder not found"}}), 500


@files.get("/file/<string:name_file>")
def get_file(name_file):
    claims = get_jwt()
    usuario = claims.get('nombre')
    folder = request.args.get("folder", "")
    ciclo = request.args.get("ciclo", "")

    file_path = path.join(PATH_FILES + ciclo, folder, name_file)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 500, "data": {"message": "Archivo no encontrado"}}), 404

    try:
        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion=f"Obtener archivo: {name_file} del folder: {folder} y ciclo: {ciclo}",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Archivos",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return send_from_directory(path.join(PATH_FILES, ciclo, folder), path=name_file, as_attachment=False)
    except FileNotFoundError:
        return jsonify({"ok": False, "status": 500, "data": {"message": "Archivo no encontrado"}}), 500


@files.get("/download/<string:name_file>")
@jwt_required()
def download_file(name_file):
    claims = get_jwt()
    usuario = claims.get('nombre')
    folder = request.args.get("folder", "")
    ciclo = request.args.get("ciclo", "")
    file_path = path.join(PATH_FILES + ciclo, folder, name_file)
    print(file_path)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 500, "data": {"message": "Archivo no encontrado"}}), 404

    # Registrar trazabilidad
    trazabilidad = Trazabilidad(
        accion=f"Descargar archivo: {name_file} de la carpeta: {folder} y ciclo: {ciclo}",
        usuario=usuario,
        fecha=datetime.now(),
        modulo="Archivos",
        nivel_alerta=1
    )
    TrazabilidadModel.add_trazabilidad(trazabilidad)

    return send_from_directory(path.join(PATH_FILES, ciclo, folder), path=name_file, as_attachment=True)


@files.delete('/delete')
@jwt_required()
def delete_file():
    claims = get_jwt()
    usuario = claims.get('nombre')
    filename = request.json.get('filename', '')
    folder = request.json.get('folder', '')
    ciclo = request.json.get('ciclo', '')

    file_path = path.join(PATH_FILES + ciclo, folder, filename)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 500, "data": {"message": "Archivo no encontrado"}}), 500
    else:
        try:
            remove(file_path)
            
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar archivo: {filename} del folder: {folder} y ciclo: {ciclo}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Archivos",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        except Exception as ex:
            return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
