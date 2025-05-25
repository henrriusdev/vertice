from decimal import Decimal
from io import BytesIO
import traceback
from flask import Blueprint, Response, jsonify, request
from weasyprint import HTML
from src.model.pago import Pago
from src.service.billetes import add_billete
from src.model.estudiante import Estudiante
from src.service.pagos import (
    generar_reporte_dia, generar_reporte_fechas, generar_reporte_monto, get_all_pagos, get_pago_by_id, add_pago, update_pago
)
from src.service.trazabilidad import add_trazabilidad
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

from src.utils.fecha import parse_fecha

pago = Blueprint("pagos_blueprint", __name__)

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
async def crear_pago():
    try:
        body = request.json

        cedula_str: str = body.get('student')
        metodo_pago: str = body.get('method')
        monto: float = body.get('amount')
        concepto: str = body.get('concept')
        fecha_pago_str: str = body.get('date')
        referencia: str = body.get('reference')
        ciclo: str = body.get('ciclo', '2025-1')
        billetes = body.get('billetes', [])
        print(cedula_str)

        # Buscar estudiante
        estudiante = await Estudiante.get(usuario__cedula=cedula_str)
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        # Mapear método de pago a ID
        metodo_pago_id = {
            "transfer": 1,
            "cash": 2,
            "point": 3
        }.get(metodo_pago, 3)

        # Crear el pago
        pago_id = await add_pago({
            "cedula_estudiante": estudiante,
            "metodo_pago_id": metodo_pago_id,
            "monto": Decimal(monto),
            "concepto": concepto,
            "fecha_pago": datetime.strptime(fecha_pago_str, "%Y-%m-%d"),
            "referencia_transferencia": referencia,
            "ciclo": ciclo
        })

        # Agregar billetes directamente
        for billete in billetes:
            billete_data = {
                "serial": billete["serial"],
                "monto": Decimal(billete["monto"]),
                "pago_id": pago_id
            }
            await add_billete(billete_data)

        return jsonify({"ok": True, "pago_id": pago_id})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


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


def pdf_response(html: str, filename: str):
    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    return Response(
        pdf_io.read(),
        mimetype='application/pdf',
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@pago.get("/reporte")
@jwt_required()
async def generar_reporte():
    tipo = request.args.get("tipo")              # dia | fechas | monto
    filtro = request.args.get("f", "")           # filtro por método
    claims = get_jwt()
    usuario = claims.get('nombre')
    print(request.args)

    if tipo == "dia":
        fecha_str = request.args.get("d")
        html = await generar_reporte_dia(fecha_str, filtro, usuario)
        return pdf_response(html, f"reporte_dia_{fecha_str}.pdf")

    elif tipo == "fechas":
        fi_str = request.args.get("fi")
        ff_str = request.args.get("ff")
        html = await generar_reporte_fechas(fi_str, ff_str, filtro, usuario)
        return pdf_response(html, f"reporte_fechas_{fi_str}_to_{ff_str}.pdf")

    elif tipo == "monto":
        fi_str = request.args.get("fi")
        ff_str = request.args.get("ff")
        html = await generar_reporte_monto(fi_str, ff_str, usuario)
        return pdf_response(html, f"reporte_montos_{fi_str}_to_{ff_str}.pdf")

    return Response("Tipo de reporte inválido", status=400)


@pago.route("/estudiante")
@jwt_required()
async def get_pagos_by_estudiante():
    cedula = request.args.get("cedula")
    if not cedula:
        return jsonify({"ok": False, "message": "Cédula requerida"}), 400
    
    # trim underscore
    cedula = cedula.replace("_", "")

    estudiante = await Estudiante.get(usuario__cedula=cedula).prefetch_related("usuario")
    if not estudiante:
        return jsonify({"ok": False, "message": "Estudiante no encontrado"}), 404

    pagos = await Pago.filter(cedula_estudiante=estudiante).prefetch_related("metodo_pago")

    resultado = []
    for pago in pagos:
        metodo = pago.metodo_pago.nombre

        # Solo buscar billetes si aplica
        billetes = []
        if metodo.lower() == "efectivo":
            from src.model.billete import Billete
            billetes_query = await Billete.filter(pago_id=pago.id)
            billetes = [{"denominacion": str(b.monto), "cantidad": 1} for b in billetes_query]

        resultado.append({
            "id": pago.id,
            "fecha": pago.fecha_pago.strftime("%d-%m-%Y"),
            "monto": str(pago.monto),
            "metodo": metodo,
            "descripcion": pago.concepto,
            "ciclo": pago.ciclo,
            "referencia": pago.referencia_transferencia,
            "estudiante": estudiante.usuario.nombre,
            "billetes": billetes
        })

    return jsonify({
        "nombre": estudiante.usuario.nombre,
        "pagos": resultado
    })


@pago.route("/total")
@jwt_required()
async def total_recaudado():
    desde = datetime.strptime(request.args.get("desde"), "%Y-%m-%d")
    hasta = datetime.strptime(request.args.get("hasta"), "%Y-%m-%d")
    pagos = (await get_all_pagos())["pagos"]

    total = sum(
        p["monto"]
        for p in pagos
        if desde <= p["fecha_pago"].replace(tzinfo=None) <= hasta
    )
    return jsonify({"ok": True, "status": 200, "total": float(total)})


@pago.route("/por-tipo")
@jwt_required()
async def pagos_por_tipo():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    pagos = (await get_all_pagos())["pagos"]

    tipos = {"transferencia": 0, "efectivo": 0, "punto": 0}
    for p in pagos:
        # Convert p["fecha_pago"] to a naive datetime object
        fecha_pago = p["fecha_pago"].replace(tzinfo=None)
        if datetime.strptime(desde, "%Y-%m-%d") <= fecha_pago <= datetime.strptime(hasta, "%Y-%m-%d"):
            nombre = p["metodo_pago"]
            if nombre == "Transferencia":
                tipos["ransferencia"] += float(p["monto"])
            elif nombre == "Efectivo":
                tipos["efectivo"] += float(p["monto"])
            elif nombre == "Punto":
                tipos["punto"] += float(p["monto"])

    return jsonify({"ok": True, "status": 200, "data": tipos})


from datetime import timedelta

@pago.route("/por-dia")
@jwt_required()
async def pagos_por_dia():
    dias = int(request.args.get("dias", 7))
    pagos = (await get_all_pagos())["pagos"]

    hoy = datetime.now()
    conteo = {}

    for i in range(dias -1, -1, -1):
        fecha = hoy - timedelta(days=i)
        conteo[fecha.strftime("%Y-%m-%d")] = 0

    for p in pagos:
        fecha_pago = p["fecha_pago"].strftime("%Y-%m-%d")
        if fecha_pago in conteo:
            conteo[fecha_pago] += float(p["monto"])

    return jsonify({"ok": True, "status": 200, "data": conteo})
