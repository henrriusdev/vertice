from flask import Blueprint, jsonify, request
from models.entities.config import Configuracion
from models.configmodel import ConfigModel
from models.trazabilidadmodel import TrazabilidadModel
from models.entities.trazabilidad import Trazabilidad
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

config = Blueprint('config_blueprint', __name__)

@config.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@config.route('/')
@jwt_required()
def get_configuraciones():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        configuraciones = ConfigModel.get_configuraciones()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener Configuraciones",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="General",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": configuraciones})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@config.route('/<id>')
def get_configuracion(id):
    try:
        configuracion = ConfigModel.get_configuracion(id)
        
        if configuracion is not None:
            return jsonify({"ok": True, "status": 200, "data": configuracion.to_JSON()})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "config no disponible"}}), 404
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@config.route('/add', methods=['POST'])
@jwt_required()
def add_configuracion():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        ciclo = request.json['ciclo']
        porc1 = request.json['porc1']
        porc2 = request.json['porc2']
        porc3 = request.json['porc3']
        horario_inicio = request.json['horario_inicio']
        horario_fin = request.json['horario_fin']
        cuota1 = request.json['cuota1']
        cuota2 = request.json['cuota2']
        cuota3 = request.json['cuota3']
        cuota4 = request.json['cuota4']
        cuota5 = request.json['cuota5']

        config = Configuracion(None, ciclo, porc1, porc2, porc3, horario_inicio, horario_fin, cuota1, cuota2, cuota3, cuota4, cuota5)
        affected_rows = ConfigModel.add_configuracion(config)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir Configuración con ciclo: {ciclo}",
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

@config.route('/update/<id>', methods=['PUT'])
@jwt_required()
def update_configuracion(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        ciclo = request.json['ciclo']
        porc1 = request.json['porc1']
        porc2 = request.json['porc2']
        porc3 = request.json['porc3']
        horario_inicio = request.json['horario_inicio']
        horario_fin = request.json['horario_fin']
        cuota1 = request.json['cuota1']
        cuota2 = request.json['cuota2']
        cuota3 = request.json['cuota3']
        cuota4 = request.json['cuota4']
        cuota5 = request.json['cuota5']

        config = Configuracion(str(id), ciclo, porc1, porc2, porc3, horario_inicio, horario_fin, cuota1, cuota2, cuota3, cuota4, cuota5)
        affected_rows = ConfigModel.update_configuracion(config)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar Configuración con id: {id}, ciclo: {ciclo}",
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
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@config.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_configuracion(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        config = Configuracion(str(id))
        affected_rows = ConfigModel.delete_configuracion(config)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar Configuración con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="General",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "confi no encontrada"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
