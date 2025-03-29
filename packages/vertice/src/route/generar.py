from flask import Blueprint, jsonify, render_template, send_file
from packages.vertice.src.service.estudiantes import StudentModel
from packages.vertice.src.service.carrera import CarreraModel
from packages.vertice.src.service.materias import MateriaModel
from flask_jwt_extended import jwt_required, get_jwt
from datetime import date, datetime
import pdfkit
import io
import traceback
import os
from packages.vertice.src.service.trazabilidad import TrazabilidadModel
from service.entities.trazabilidad import Trazabilidad

generar_pdf = Blueprint('generar_blueprint', __name__)

@generar_pdf.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

BINPATH = os.getenv('BINPATH', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

@generar_pdf.route('/<cedula>')
def generar(cedula):
    try:
        student = StudentModel.get_student(cedula)
        if student is not None:
            notas = StudentModel.get_materias_inscritas(cedula)
            carrera = CarreraModel.get_carrera(student["carrera"])
            config = pdfkit.configuration(wkhtmltopdf=BINPATH)

            student["carrera"] = carrera["nombre"]
            fecha_actual = date.today().strftime("%d/%m/%Y")
            res = render_template('fichaEstudiantes.html', student=student, materias=notas["contenido"], fecha_actual=fecha_actual)
            pdf = pdfkit.from_string(res, configuration=config, options={"enable-local-file-access": True})
            pdf_blob = io.BytesIO(pdf)

            return send_file(path_or_file=pdf_blob, download_name="ficha_estudiantil.pdf", as_attachment=True)
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}), 500

@generar_pdf.route('/docenteria')
def docenteria():
    try:
        join = MateriaModel.get_docenteria()
        if join is not None:
            config = pdfkit.configuration(wkhtmltopdf=BINPATH)
            fecha_actual = date.today().strftime("%d/%m/%Y")
            res = render_template('docenteria.html', materias=join, fecha_actual=fecha_actual)
            pdf = pdfkit.from_string(res, configuration=config, options={"enable-local-file-access": True})
            pdf_blob = io.BytesIO(pdf)

            return send_file(path_or_file=pdf_blob, download_name="docentes_materias.pdf", as_attachment=True)
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Datos no encontrados"}}), 404
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}), 500
