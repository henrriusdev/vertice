from flask import Blueprint, request, jsonify, send_from_directory, send_file, render_template
from flask_jwt_extended import jwt_required, get_jwt
from os import getcwd, path, remove, makedirs, listdir
from datetime import date
from io import BytesIO
from weasyprint import HTML
import traceback

from src.model import Configuracion
from src.service.trazabilidad import add_trazabilidad
from src.service.materias import listar_materias_asignadas, get_materia_con_nombre_y_config, get_estudiantes_con_notas
from src.service.usuarios import get_usuario_por_correo

arc = Blueprint("archivo", __name__)
PATH_FILES = path.abspath(path.join(getcwd(), "../../uploads/planificacion/"))


def create_folder_if_not_exists(folder_path):
    if not path.exists(folder_path):
        makedirs(folder_path)


# ----------------------- ARCHIVOS -----------------------

@arc.post("/planificacion")
@jwt_required()
async def upload_file():
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))

        file = request.files['file']
        ciclo = request.form.get('ciclo', '')
        folder = request.form.get('folder', '')

        ciclo_path = path.join(PATH_FILES, ciclo)
        create_folder_if_not_exists(ciclo_path)

        folder_path = path.join(ciclo_path, folder)
        create_folder_if_not_exists(folder_path)

        file.save(path.join(folder_path, file.filename))

        # Trazabilidad
        await add_trazabilidad({
            "accion": f"Subir archivo: {file.filename} a carpeta: {folder}, ciclo: {ciclo}",
            "usuario": usuario,
            "modulo": "Archivos",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "message": str(ex)}), 500


@arc.get("/download/<folder>")
@jwt_required()
async def download_file(folder: str):
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))
        ciclo = (await Configuracion.get(id=1)).ciclo

        folder_path = path.join(PATH_FILES, ciclo, folder)

        if not path.exists(folder_path):
            return jsonify({"ok": False, "status": 404, "data": {"message": "Carpeta no encontrada"}}), 404

        # Obtener único archivo dentro de la carpeta
        archivos = [f for f in listdir(folder_path) if path.isfile(path.join(folder_path, f))]

        if not archivos:
            return jsonify({"ok": False, "status": 404, "data": {"message": "No hay archivos en la carpeta"}}), 404

        if len(archivos) > 1:
            return jsonify({"ok": False, "status": 400, "data": {"message": "Hay más de un archivo en la carpeta"}}), 400

        archivo = archivos[0]
        file_path = path.join(folder_path, archivo)
        print("Descargando:", file_path)

        # Trazabilidad
        await add_trazabilidad({
            "accion": f"Descargar archivo: {archivo} de carpeta: {folder}, ciclo: {ciclo}",
            "usuario": usuario,
            "modulo": "Archivos",
            "nivel_alerta": 1
        })

        return send_file(file_path, download_name=archivo, as_attachment=True)

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@arc.delete('/delete')
@jwt_required()
async def delete_file():
    claims = get_jwt()
    usuario = await get_usuario_por_correo(claims.get('sub'))
    filename = request.json.get('filename', '')
    folder = request.json.get('folder', '')
    ciclo = request.json.get('ciclo', '')

    file_path = path.join(PATH_FILES + ciclo, folder, filename)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 404, "data": {"message": "Archivo no encontrado"}}), 404

    try:
        remove(file_path)

        # Trazabilidad
        await add_trazabilidad({
            "accion": f"Eliminar archivo: {filename} de carpeta: {folder}, ciclo: {ciclo}",
            "usuario": usuario,
            "modulo": "Archivos",
            "nivel_alerta": 3
        })

        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


# ----------------------- PDF -----------------------

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


@arc.get('/notas/<string:materia_id>/reporte')
@jwt_required()
async def reporte_notas_pdf(materia_id):
    try:
        claims = get_jwt()
        correo = claims.get("sub")
        nombre_docente = claims.get("nombre")

        # 1. Obtener datos necesarios
        materia = await get_materia_con_nombre_y_config(materia_id, correo)
        estudiantes = await get_estudiantes_con_notas(materia_id)

        if not materia or not estudiantes:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Datos no encontrados"}}), 404

        num_cortes = materia["num_cortes"]

        # 2. Renderizar HTML
        html = render_template(
            "reporte_notas.html",
            materia=materia,
            docente={"nombre": nombre_docente},
            estudiantes=estudiantes,
            num_cortes=num_cortes
        )

        # 3. Convertir a PDF
        pdf = HTML(string=html).write_pdf()

        # 4. Enviar como blob
        filename = f"reporte_calificaciones_{materia['id']}.pdf"
        return send_file(BytesIO(pdf), download_name=filename, as_attachment=True)

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
