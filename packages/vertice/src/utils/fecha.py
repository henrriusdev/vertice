import datetime
import pytz
from num2words import num2words
from src.settings import settings


def parse_fecha(fecha_str: str) -> datetime:
    return datetime.datetime.strptime(fecha_str, "%d/%m/%Y")


def parse_fecha_with_timezone(fecha_str: str, format: str = "%Y-%m-%d") -> datetime.datetime:
    """Parse a date string and convert it to Venezuela timezone"""
    dt = datetime.datetime.strptime(fecha_str, format)
    # Assume the input date is in Venezuela timezone and make it timezone-aware
    venezuela_tz = settings.timezone_obj
    return venezuela_tz.localize(dt)


def now_in_venezuela() -> datetime.datetime:
    """Get current datetime in Venezuela timezone"""
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    return utc_now.astimezone(settings.timezone_obj)


def to_venezuela_timezone(dt: datetime.datetime) -> datetime.datetime:
    """Convert a datetime to Venezuela timezone"""
    if dt.tzinfo is None:
        # If naive datetime, assume it's UTC
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(settings.timezone_obj)

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
