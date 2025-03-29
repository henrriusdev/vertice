import traceback
from service.entities.peticiones import Peticiones
from packages.vertice.src.service.peticiones import PeticionesModel
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from packages.vertice.src.service.trazabilidad import TrazabilidadModel
from service.entities.trazabilidad import Trazabilidad

peticion = Blueprint('peticion_blueprint', __name__)

@peticion.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@peticion.route('/')
@jwt_required()
def get_peticiones():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        peticiones = PeticionesModel.get_peticiones()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener todas las Peticiones",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Peticiones",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": peticiones})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@peticion.route('/<id>')
@jwt_required()
def get_peticion(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        peticiones = PeticionesModel.get_peticion(id)
        
        if peticiones is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener Petición con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Peticiones",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": peticiones})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "peticion no disponible"}}), 404
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@peticion.route('/pendientes')
@jwt_required()
def get_peticiones_pendientes():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        peticiones_pendientes = PeticionesModel.get_peticiones_pendientes()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener todas las Peticiones Pendientes",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Peticiones",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": peticiones_pendientes})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@peticion.route('/add', methods=["POST"])
@jwt_required()
def add_peticion():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        id_docente = request.json['id_docente']
        descripcion = request.json['descripcion']
        estado = request.json['estado']
        if estado not in ["Aprobado", "Denegado", "Pendiente"]:
            return jsonify({'error': 'Valor inválido para el campo estado'}), 400
        id_estudiante = request.json['id_estudiante']
        id_materia = request.json['id_materia']
        campo = request.json['campo']

        peticion = Peticiones(None, id_docente, descripcion, estado, id_estudiante, id_materia, campo)
        affected_rows = PeticionesModel.add_peticion(peticion)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir Petición para el estudiante con cédula: {id_estudiante}, materia: {id_materia}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Peticiones",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@peticion.route('/update/<id>', methods=["PATCH"])
def update_peticion(id):
    try:
        data = request.json

        # Definimos una lista de campos permitidos para actualizar.
        allowed_fields = ["id_docente", "descripcion", "estado", "id_estudiante", "id_materia", "campo"]

        # Filtramos los campos proporcionados en la solicitud para asegurarnos de que solo se actualicen los campos permitidos.
        fields_to_update = {field: data[field] for field in allowed_fields if field in data}

        # Si no se proporcionan campos permitidos para actualizar, devolvemos un error con código 400.
        if not fields_to_update:
            return jsonify({"error": "No se proporcionaron campos válidos para actualizar"}), 400

        # Agregamos el ID de la solicitud a los campos a actualizar para asegurarnos de que actualicemos la solicitud correcta.
        fields_to_update["id"] = id
        peticion = Peticiones(**fields_to_update)

        # Llamamos a la función update_peticion del modelo para actualizar la solicitud en la base de datos.
        affected_rows = PeticionesModel.update_peticion(peticion)

        if affected_rows == 1:
            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@peticion.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_peticion(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        peticion = Peticiones(str(id))
        affected_rows = PeticionesModel.delete_peticion(peticion)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar Petición con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Peticiones",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "peticion no encontrada"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
