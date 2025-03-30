from src.model.configuracion import Configuracion


async def get_configuracion(id: int):
    try:
        config = await Configuracion.get_or_none(id=id)
        return config
    except Exception as ex:
        raise Exception(ex)

async def add_configuracion(config_data):
    try:
        nueva_config = await Configuracion.create(
            ciclo=config_data.ciclo,
            num_porcentaje=config_data.porc3,  # ajusta esto si cambia
            num_cuotas=5,
            horario_inicio=config_data.horario_inicio,
            horario_fin=config_data.horario_fin,
            cuotas={
                "cuota1": config_data.cuota1,
                "cuota2": config_data.cuota2,
                "cuota3": config_data.cuota3,
                "cuota4": config_data.cuota4,
                "cuota5": config_data.cuota5,
            }
        )
        return nueva_config.id
    except Exception as ex:
        raise Exception(ex)

async def update_configuracion(config_data):
    try:
        config = await Configuracion.get_or_none(id=config_data.id)
        if not config:
            return 0

        config.ciclo = config_data.ciclo
        config.horario_inicio = config_data.horario_inicio
        config.horario_fin = config_data.horario_fin
        config.cuotas = {
            "cuota1": config_data.cuota1,
            "cuota2": config_data.cuota2,
            "cuota3": config_data.cuota3,
            "cuota4": config_data.cuota4,
            "cuota5": config_data.cuota5,
        }
        await config.save()
        return 1
    except Exception as ex:
        raise Exception(ex)
