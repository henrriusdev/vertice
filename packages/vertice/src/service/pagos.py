# services/pagos_service.py
from src.model.pago import Pago

async def get_all_pagos():
    result = {"pagos": [], "metodos": []}
    
    pagos = await Pago.all().prefetch_related("metodo_pago", "cedula_estudiante")

    for pago in pagos:
        result["pagos"].append({
            "id": pago.id,
            "cedula_estudiante": pago.cedula_estudiante.usuario.cedula,
            "monto": pago.monto,
            "concepto": pago.concepto,
            "fecha_pago": pago.fecha_pago,
            "ciclo": pago.ciclo
        })
        result["metodos"].append({
            "id": pago.metodo_pago.id,
            "nombre": pago.metodo_pago.nombre
        })
    
    return result


async def get_pago_by_id(pago_id: int):
    pago = await Pago.get(id=pago_id).prefetch_related("cedula_estudiante", "metodo_pago")
    
    if not pago:
        return None

    return {
        "pago": {
            "id": pago.id,
            "cedula_estudiante": pago.cedula_estudiante.usuario.cedula,
            "monto": pago.monto,
            "concepto": pago.concepto,
            "fecha_pago": pago.fecha_pago,
            "ciclo": pago.ciclo
        },
        "estudiante": {
            "id": pago.cedula_estudiante.id,
            "fullname": pago.cedula_estudiante.usuario.fullname,
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
    deleted = await Pago.filter(id=pago_id).delete()
    return deleted
