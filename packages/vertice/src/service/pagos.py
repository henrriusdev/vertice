# services/pagos_service.py
from datetime import datetime
from src.model.pago import Pago
from tortoise.expressions import Q
from src.utils.reporte_pdf import generar_html_reporte, generar_html_montos
from src.utils.fecha import to_venezuela_timezone, parse_fecha_with_timezone

async def get_all_pagos():
    result = {"pagos": [], "metodos": []}
    
    pagos = await Pago.all().prefetch_related("metodo_pago", "cedula_estudiante__usuario")

    for pago in pagos:
        # Convert the stored datetime to Venezuela timezone for display
        fecha_venezuela = to_venezuela_timezone(pago.fecha_pago)
        
        result["pagos"].append({
            "id": pago.id,
            "cedula_estudiante": pago.cedula_estudiante.usuario.cedula,
            "monto": pago.monto,
            "concepto": pago.concepto,
            "fecha_pago": fecha_venezuela,
            "ciclo": pago.ciclo,
            "metodo_pago": pago.metodo_pago.nombre,
        })
    
    return result


async def get_pago_by_id(pago_id: int):
    pago = await Pago.get(id=pago_id).prefetch_related("cedula_estudiante", "metodo_pago")
    
    if not pago:
        return None

    # Convert the stored datetime to Venezuela timezone for display
    fecha_venezuela = to_venezuela_timezone(pago.fecha_pago)

    return {
        "pago": {
            "id": pago.id,
            "cedula_estudiante": pago.cedula_estudiante.usuario.cedula,
            "monto": pago.monto,
            "concepto": pago.concepto,
            "fecha_pago": fecha_venezuela,
            "ciclo": pago.ciclo
        },
        "estudiante": {
            "id": pago.cedula_estudiante.id,
            "nombre": pago.cedula_estudiante.usuario.nombre,
            "correo": pago.cedula_estudiante.usuario.correo
        },
        "metodo": {
            "id": pago.metodo_pago.id,
            "nombre": pago.metodo_pago.nombre
        }
    }


async def add_pago(data):
    pago = await Pago.create(**data)
    return pago.id


async def update_pago(pago_id: int, data: dict):
    updated = await Pago.filter(id=pago_id).update(**data)
    return updated


async def delete_pago(pago_id: int):
    pago = await Pago.get(id=pago_id)
    pago.activo = False
    await pago.save()
    return 1

async def generar_reporte_dia(fecha_str: str, filtro: str | None, usuario: str):    
    fecha = parse_fecha_with_timezone(fecha_str, "%Y-%m-%d")
    
    # Create start and end of day in Venezuela timezone
    inicio_dia = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = fecha.replace(hour=23, minute=59, second=59, microsecond=999999)

    q = Q(fecha_pago__gte=inicio_dia, fecha_pago__lte=fin_dia)
    if filtro:
        q &= Q(metodo_pago__nombre=filtro)

    pagos = await Pago.filter(q).prefetch_related("cedula_estudiante__usuario", "metodo_pago")

    return generar_html_reporte(
        pagos, usuario, "Día", filtro if filtro else "Todos", fecha.strftime("%d/%m/%Y")
    )


async def generar_reporte_fechas(fi_str: str, ff_str: str, filtro: str | None, usuario: str):
    fi = parse_fecha_with_timezone(fi_str, "%Y-%m-%d")
    ff = parse_fecha_with_timezone(ff_str, "%Y-%m-%d")

    # Create start and end of day range in Venezuela timezone
    inicio_dia = fi.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = ff.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    q = Q(fecha_pago__gte=inicio_dia, fecha_pago__lte=fin_dia)
    if filtro:
        q &= Q(metodo_pago__nombre=filtro)

    pagos = await Pago.filter(q).prefetch_related("cedula_estudiante__usuario", "metodo_pago")

    return generar_html_reporte(
        pagos, usuario, "Fechas específicas", filtro if filtro else "Todos",
        f"{fi.strftime('%d/%m/%Y')} a {ff.strftime('%d/%m/%Y')}"
    )


async def generar_reporte_monto(fi_str: str, ff_str: str, usuario: str):
    fi = parse_fecha_with_timezone(fi_str, "%Y-%m-%d")
    ff = parse_fecha_with_timezone(ff_str, "%Y-%m-%d")

    # Create start and end of day range in Venezuela timezone
    inicio_dia = fi.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = ff.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    q = Q(fecha_pago__gte=inicio_dia, fecha_pago__lte=fin_dia)
    pagos = await Pago.filter(q).prefetch_related("metodo_pago")

    return generar_html_montos(
        pagos, usuario, f"{fi.strftime('%d/%m/%Y')} a {ff.strftime('%d/%m/%Y')}"
    )
