from src.model.trazabilidad import Trazabilidad
from datetime import datetime

async def add_trazabilidad(data: dict):
    await Trazabilidad.create(
        accion=data["accion"],
        usuario=data["usuario"],
        fecha=data.get("fecha", datetime.now()),
        modulo=data["modulo"],
        nivel_alerta=data.get("nivel_alerta", 1)
    )
    return True


async def get_trazabilidad():
    trazas = await Trazabilidad.all().order_by("-fecha")
    return [
        {
            "id": t.id,
            "accion": t.accion,
            "usuario": t.usuario,
            "fecha": t.fecha,
            "modulo": t.modulo,
            "nivel_alerta": t.nivel_alerta
        } for t in trazas
    ]
