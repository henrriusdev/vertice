from datetime import datetime


def parse_fecha(fecha_str: str) -> datetime:
    return datetime.strptime(fecha_str, "%d/%m/%Y")

def format_fecha(fecha: datetime):
    return fecha.strftime("%d/%m/%Y")