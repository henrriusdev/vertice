from flask import Blueprint, jsonify, request
from packages.vertice.src.service.pagos import (
    get_all_pagos, get_pago_by_id, add_pago, update_pago
)
from service.trazabilidad import add_trazabilidad
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

pago = Blueprint("pagos_blueprint", __name__)

@pago.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@pago.route("/")
@jwt_required()
async def get_pagos():
    claims = get_jwt()
    usuario = claims.get('nombre')
    pagos = await get_all_pagos()

    await add_trazabilidad({
        "accion": "Obtener todos los pagos",
        "usuario": usuario,
        "modulo": "Administración",
        "nivel_alerta": 1
    })

    return jsonify({"ok": True, "status": 200, "data": pagos})


@pago.route("/<int:id>")
@jwt_required()
async def get_pago(id):
    claims = get_jwt()
    usuario = claims.get('nombre')

    pago = await get_pago_by_id(id)
    if pago:
        await add_trazabilidad({
            "accion": f"Obtener pago con id: {id}",
            "usuario": usuario,
            "modulo": "Administración",
            "nivel_alerta": 1
        })
        return jsonify({"ok": True, "status": 200, "data": pago})
    else:
        return jsonify({"ok": False, "status": 404, "data": {"message": "Pago no encontrado"}}), 404


@pago.route("/add", methods=["POST"])
@jwt_required()
async def add_pago_route():
    claims = get_jwt()
    usuario = claims.get('nombre')

    data = {
        "cedula_estudiante_id": request.json['cedula_estudiante_id'],
        "metodo_pago_id": request.json['metodo_pago_id'],
        "monto": request.json['monto'],
        "concepto": request.json["concepto"],
        "fecha_pago": request.json['fecha_pago'],
        "referencia_transferencia": request.json.get('referencia_transferencia'),
        "ciclo": request.json.get('ciclo')
    }

    pago_id = await add_pago(data)

    await add_trazabilidad({
        "accion": f"Añadir pago para estudiante: {data['cedula_estudiante_id']} monto: {data['monto']}",
        "usuario": usuario,
        "modulo": "Administración",
        "nivel_alerta": 2
    })

    return jsonify({"ok": True, "status": 200, "data": {"pagoId": pago_id}})


@pago.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
async def update_pago_route(id):
    claims = get_jwt()
    usuario = claims.get('nombre')

    data = {
        "cedula_estudiante_id": request.json['cedula_estudiante_id'],
        "metodo_pago_id": request.json['metodo_pago_id'],
        "monto": request.json['monto'],
        "concepto": request.json['concepto'],
        "fecha_pago": request.json['fecha_pago'],
        "referencia_transferencia": request.json.get('referencia_transferencia'),
        "ciclo": request.json.get('ciclo')
    }

    updated = await update_pago(id, data)

    if updated:
        await add_trazabilidad({
            "accion": f"Actualizar pago con id: {id} para estudiante: {data['cedula_estudiante_id']}",
            "usuario": usuario,
            "modulo": "Administración",
            "nivel_alerta": 2
        })
        return jsonify({"ok": True, "status": 200, "data": None})
    else:
        return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar"}}), 500
