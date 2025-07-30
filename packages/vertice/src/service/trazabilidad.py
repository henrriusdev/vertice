from src.model.trazabilidad import Trazabilidad
from datetime import datetime, time
from tortoise.expressions import Q
from src.utils.fecha import now_in_venezuela, to_venezuela_timezone

async def add_trazabilidad(data: dict):
    await Trazabilidad.create(
        accion=data["accion"],
        usuario=data["usuario"],
        fecha=data.get("fecha", now_in_venezuela()),
        modulo=data["modulo"],
        nivel_alerta=data.get("nivel_alerta", 1)
    )
    return True


async def get_trazabilidad(filtros: dict):
    query = Q()

    if filtros.get("busqueda"):
        q = filtros["busqueda"].lower()
        query &= Q(usuario__nombre__icontains=q) | Q(usuario__correo__icontains=q) | Q(modulo__icontains=q) | Q(accion__icontains=q)

    if filtros.get("rol"):
        query &= Q(usuario__rol__nombre__iexact=filtros["rol"])

    if filtros.get("fechaDesde"):
        from src.utils.fecha import parse_fecha_with_timezone
        fecha = parse_fecha_with_timezone(filtros["fechaDesde"], "%Y-%m-%d")
        desde = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
        query &= Q(fecha__gte=desde)

    if filtros.get("fechaHasta"):
        from src.utils.fecha import parse_fecha_with_timezone
        fecha = parse_fecha_with_timezone(filtros["fechaHasta"], "%Y-%m-%d")
        hasta = fecha.replace(hour=23, minute=59, second=59, microsecond=999999)
        query &= Q(fecha__lte=hasta)

    trazas = await Trazabilidad.filter(query).order_by("-fecha").prefetch_related("usuario", "usuario__rol")

    return [
        {
            "id": t.id,
            "accion": t.accion,
            "usuario": t.usuario.nombre,
            "correo": t.usuario.correo,
            "rol": t.usuario.rol.nombre,
            "fecha": to_venezuela_timezone(t.fecha),
            "modulo": t.modulo,
            "nivel_alerta": t.nivel_alerta
        }
        for t in trazas
    ]