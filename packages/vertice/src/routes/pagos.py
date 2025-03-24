from flask import Blueprint, jsonify, request
from services.entities.pagos import Pago
from services.pagosmodel import PagoModel
from services.entities.monto import Monto
from services.mountmodel import MountModel
from services.metodomodel import MetodoModel
from services.entities.metodo import Metodo
from services.transferenciamodel import TransferenciaModel
from services.entities.transferencias import Transferencia
from traceback import print_exc
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from services.trazabilidadmodel import TrazabilidadModel
from services.entities.trazabilidad import Trazabilidad

pago = Blueprint("pagos_blueprint", __name__)

@pago.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response

@pago.route("/")
@jwt_required()
def get_pagos():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        pagos = PagoModel.get_pagos()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener todos los pagos",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Administración",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": pagos})
    except Exception as ex:
        print(ex)
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@pago.route("/<id>")
@jwt_required()
def get_pago(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        pago = PagoModel.get_pago(id)
        
        if pago is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener pago con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Administración",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": pago})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Pago no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@pago.route("/add", methods=["POST"])
@jwt_required()
def add_pago():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cedula_estudiante = request.json['cedula_estudiante']
        descripcion = request.json["descripcion"]
        metodo_pago = request.json['metodo']
        monto = request.json['monto']
        fecha_pago = request.json['fecha_pago']
        referencia_transferencia = request.json.get('referencia_transferencia', None)
        
        metodo = Metodo(None, metodo_pago, descripcion)
        metodo_id = MetodoModel.add_metodo(metodo)

        monto = Monto(None, descripcion, monto)
        monto_id = MountModel.add_monto(monto)
        id_trans = None
        if referencia_transferencia is not None:
            transf = Transferencia(None, str(referencia_transferencia))
            id_trans = TransferenciaModel.add_transferencia(transf)

        pago = Pago(None, cedula_estudiante, metodo_id, monto_id, fecha_pago, id_trans)
        pagos, id_pago = PagoModel.add_pago(pago)

        if pagos == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir pago para el estudiante con cédula: {cedula_estudiante}, monto: {monto}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Administración",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": {"pagoId": id_pago}})
        else:
            return jsonify({"ok": False, "status": 500, "data": None}), 500
    except Exception as ex:
        print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@pago.route("/update/<id>", methods=["PUT"])
@jwt_required()
def update_pago(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cedula_estudiante = request.json['cedula_estudiante']
        metodo_pago_id = request.json['metodo_pago_id']
        monto_id = request.json['monto_id']
        fecha_pago = request.json['fecha_pago']
        referencia_transferencia = request.json['referencia_transferencia']

        pago = Pago(str(id), cedula_estudiante, metodo_pago_id, monto_id, fecha_pago, referencia_transferencia)
        pagos = PagoModel.update_pago(pago)

        if pagos == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar pago con id: {id} para el estudiante con cédula: {cedula_estudiante}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Administración",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos ingresados"}}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

