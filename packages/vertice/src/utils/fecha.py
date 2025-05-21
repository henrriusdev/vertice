import datetime

from num2words import num2words


def parse_fecha(fecha_str: str) -> datetime:
    return datetime.datetime.strptime(fecha_str, "%d/%m/%Y")

def format_fecha(fecha: datetime.datetime):
    return fecha.strftime("%d/%m/%Y")


def generar_fecha_larga(fecha: datetime.date = None):
    if fecha is None:
        fecha = datetime.date.today()

    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    dia = fecha.day
    mes = meses[fecha.month - 1]
    anio = fecha.year

    # Día en texto
    if dia == 1:
        dia_texto = "el 1er día"
    else:
        dia_texto = f"a los {dia} días"

    # Año en texto
    anio_letras = num2words(anio, lang='es').replace("uno", "un")

    return f"{dia_texto} del mes de {mes} del año {anio_letras}"
