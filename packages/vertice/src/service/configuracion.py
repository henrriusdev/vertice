from src.utils.fecha import parse_fecha
from src.model.configuracion import Configuracion


async def get_configuracion(id: int = 1):
    try:
        config = await Configuracion.get_or_none(id=id)
        data = {
            "ciclo": config.ciclo,
            "num_porcentaje": config.num_porcentaje,
            "num_cuotas": config.num_cuotas,
            "horario_inicio": config.horario_inicio,
            "horario_fin": config.horario_fin,
            "cuotas": config.cuotas,
            "porcentajes": config.porcentajes
        }
        return data
    except Exception as ex:
        raise Exception(str(ex))


async def add_configuracion(config_data: dict):
    try:
        nueva_config = await Configuracion.create(
            ciclo=config_data["ciclo"],
            num_porcentaje=config_data["num_porcentaje"],
            num_cuotas=config_data["num_cuotas"],
            horario_inicio=config_data["horario_inicio"],
            horario_fin=config_data["horario_fin"],
            cuotas=config_data["cuotas"],  # se espera un array/lista
            porcentajes=config_data["porcentajes"]  # se espera un array/lista
        )
        return nueva_config.id
    except Exception as ex:
        raise Exception(str(ex))


async def update_configuracion(config_data: dict):
    try:
        print(config_data)
        config = await Configuracion.get_or_none(id=1)
        if not config:
            return 0

        config.ciclo = config_data["ciclo"]
        config.num_porcentaje = config_data["num_porcentaje"]
        config.num_cuotas = config_data["num_cuotas"]
        config.horario_inicio = parse_fecha(config_data["horario_inicio"])
        config.horario_fin = parse_fecha(config_data["horario_fin"])
        config.cuotas = config_data["cuotas"]
        config.porcentajes = config_data["porcentajes"]

        await config.save()
        return 1
    except Exception as ex:
        raise Exception(str(ex))
