from flask import Blueprint, jsonify, request
from services.carreramodel import CarreraModel
from services.entities.carreras import Carrera
from services.trazabilidadmodel import TrazabilidadModel
from services.entities.trazabilidad import Trazabilidad
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
import traceback

# no se q hago, pero luzco bien haciendolo :*

carrera = Blueprint('carrera_blueprint', __name__)

@carrera.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@carrera.route('/')
@jwt_required()
def get_carreras():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        carreras = CarreraModel.get_carreras()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener Carreras",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="General",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": carreras})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}), 500

@carrera.route('/<id>')
@jwt_required()
def get_carrera(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        carrera = CarreraModel.get_carrera(id)
        
        if carrera is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener Carrera con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="General",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": carrera})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "carrera no encontrada"}}), 404
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@carrera.route('/add', methods=['POST'])
@jwt_required()
def add_carrera():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        id = request.json['id']
        nombre = request.json['nombre']

        carrera = Carrera(str(id), nombre)
        affected_rows = CarreraModel.add_carrera(carrera)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir Carrera con id: {id}, nombre: {nombre}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="General",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@carrera.route('/update/<id>', methods=['PUT'])
@jwt_required()
def update_carrera(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        nombre = request.json['nombre']
        carrera = Carrera(str(id), nombre)
        affected_rows = CarreraModel.update_carrera(carrera)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar Carrera con id: {id}, nombre: {nombre}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="General",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@carrera.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_carrera(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        carrera = Carrera(str(id))
        affected_rows = CarreraModel.delete_carrera(carrera)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar Carrera con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="General",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "carrera no encontrada"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
