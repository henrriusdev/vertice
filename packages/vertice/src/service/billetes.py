from src.model.billete import Billete

async def get_billetes():
    return await Billete.all().values("id", "serial", "monto", "pago_id")

async def get_billete(id: int):
    billete = await Billete.filter(id=id).values("id", "serial", "monto", "pago_id").first()
    if billete:
        return billete
    raise Exception("Billete no existe")

async def add_billete(data):
    billete = await Billete.create(**data)
    return billete.id

async def update_billete(id: int, data):
    updated = await Billete.filter(id=id).update(**data)
    if updated == 0:
        raise Exception("Billete no encontrado")
    return updated
