from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from collections import defaultdict

# Configura el loader apuntando a la carpeta templates
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "template"
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

# ─────────────────────────────────────────────
# Reporte detallado de pagos (día / fechas)
def generar_html_reporte(pagos, usuario, tipo_reporte, metodo, fecha_filtro):
    template = env.get_template("reporte_pagos.html")
    total = sum([float(p.monto) for p in pagos])

    return template.render(
        usuario=usuario,
        fecha_actual=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        tipo_reporte=tipo_reporte,
        metodo=metodo,
        fecha_filtro=fecha_filtro,
        pagos=pagos,
        monto_total=total
    )

# ─────────────────────────────────────────────
# Reporte resumen de montos agrupado por método
def generar_html_montos(pagos, usuario, fecha_rango):
    template = env.get_template("reporte_montos.html")
    totales = defaultdict(float)

    for p in pagos:
        totales[p.metodo_pago.nombre] += float(p.monto)

    gran_total = sum(totales.values())

    return template.render(
        usuario=usuario,
        fecha_actual=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        fecha_rango=fecha_rango,
        totales=totales,
        gran_total=gran_total
    )
