import traceback
from datetime import datetime, timedelta
from decimal import Decimal
from io import BytesIO

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from weasyprint import HTML

from src.model.estudiante import Estudiante
from src.model.pago import Pago
from src.service.billetes import add_billete
from src.service.pagos import (
    generar_reporte_dia, generar_reporte_fechas, generar_reporte_monto, get_all_pagos, get_pago_by_id, add_pago,
    update_pago
)
from src.service.trazabilidad import add_trazabilidad
from src.utils.reporte_pdf import env

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
        tasa_divisa: float | None = body.get('exchange_rate')
        ciclo: str = body.get('ciclo', '2025-1')
        billetes = body.get('billetes', [])
        print(cedula_str)

        # Buscar estudiante
        estudiante = await Estudiante.get(usuario__cedula=cedula_str).prefetch_related("usuario", "carrera")
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        # Mapear método de pago a ID
        metodo_pago_id = {
            "transfer": 1,
            "cash": 2,
            "point": 3
        }.get(metodo_pago, 3)
        
        # Mapear método de pago a nombre legible
        metodo_pago_nombre = {
            "transfer": "Transferencia",
            "cash": "Efectivo",
            "point": "Punto de Venta"
        }.get(metodo_pago, "Otro")

        # Crear el pago
        pago_id = await add_pago({
            "cedula_estudiante": estudiante,
            "metodo_pago_id": metodo_pago_id,
            "monto": Decimal(monto),
            "concepto": concepto,
            "fecha_pago": datetime.strptime(fecha_pago_str, "%Y-%m-%d"),
            "referencia_transferencia": referencia,
            "ciclo": ciclo,
            "tasa_divisa": Decimal(tasa_divisa) if tasa_divisa else None
        })

        # Agregar billetes directamente
        billetes_guardados = []
        for billete in billetes:
            billete_data = {
                "serial": billete["serial"],
                "monto": Decimal(billete["monto"]),
                "pago_id": pago_id
            }
            await add_billete(billete_data)
            billetes_guardados.append(billete_data)

        # Obtener datos del usuario (cajero)
        claims = get_jwt()
        cajero = claims.get('nombre', 'Usuario del Sistema')
        
        # Calcular monto en USD
        monto_decimal = Decimal(monto)
        tasa_decimal = Decimal(tasa_divisa) if tasa_divisa else Decimal('1')
        monto_usd = monto_decimal / tasa_decimal if tasa_decimal else Decimal('0')
        
        # Obtener datos adicionales del estudiante
        carrera = await estudiante.carrera
        usuario = await estudiante.usuario
        
        # Preparar datos para la plantilla
        estudiante_data = {
            "nombre": usuario.nombre,
            "cedula": usuario.cedula,
            "carrera": carrera.nombre if carrera else "No especificada"
        }
        
        # Generar HTML para la constancia de pago
        template = env.get_template("constancia_pago.html")
        html = template.render(
            fecha_emision=datetime.now().strftime("%d/%m/%Y"),
            pago_id=pago_id,
            estudiante=estudiante_data,
            concepto=concepto,
            fecha_pago=datetime.strptime(fecha_pago_str, "%Y-%m-%d").strftime("%d/%m/%Y"),
            monto=str(monto_decimal),
            tasa_divisa=str(tasa_decimal),
            monto_usd=str(round(monto_usd, 2)),
            metodo_pago=metodo_pago_nombre,
            metodo_pago_id=metodo_pago_id,
            referencia=referencia,
            billetes=billetes_guardados,
            cajero=cajero
        )
        
        # Generar y devolver el PDF
        return pdf_response(html, f"constancia_pago_{pago_id}.pdf")

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


def pdf_response(html: str, filename: str, as_json=True):
    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)
    
    if as_json:
        import base64
        pdf_bytes = pdf_io.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return jsonify({
            "type": "application/pdf",
            "base64": pdf_base64,
            "message": "Constancia de pago generada exitosamente"
        })
    else:
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
    claims = get_jwt()
    usuario = claims.get('nombre')

    tipo = request.args.get("tipo")
    filtro = request.args.get("f")
    as_json = request.args.get("json", "true").lower() == "true"

    if tipo == "dia":
        fecha_str = request.args.get("d")
        html = await generar_reporte_dia(fecha_str, filtro, usuario)
        return pdf_response(html, f"reporte_dia_{fecha_str}.pdf", as_json=as_json)

    elif tipo == "fechas":
        fi_str = request.args.get("fi")
        ff_str = request.args.get("ff")
        html = await generar_reporte_fechas(fi_str, ff_str, filtro, usuario)
        return pdf_response(html, f"reporte_fechas_{fi_str}_to_{ff_str}.pdf", as_json=as_json)

    elif tipo == "monto":
        fi_str = request.args.get("fi")
        ff_str = request.args.get("ff")
        html = await generar_reporte_monto(fi_str, ff_str, usuario)
        return pdf_response(html, f"reporte_montos_{fi_str}_to_{ff_str}.pdf", as_json=as_json)

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
            "tasa": str(pago.tasa_divisa) if pago.tasa_divisa else None,
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
