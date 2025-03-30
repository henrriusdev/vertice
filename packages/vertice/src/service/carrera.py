from src.model.carrera import Carrera

async def get_carreras():
    return await Carrera.all().values("id", "nombre")

async def get_carrera(id: int):
    carrera = await Carrera.filter(id=id).values("id", "nombre").first()
    if not carrera:
        raise Exception("Carrera no encontrada")
    return carrera

async def add_carrera(data):
    existe = await Carrera.get_or_none(id=data["id"])
    if existe:
        raise Exception("Carrera ya existe")
    carrera = await Carrera.create(**data)
    return carrera.id

async def update_carrera(id: int, data):
    updated = await Carrera.filter(id=id).update(**data)
    if updated == 0:
        raise Exception("Carrera no encontrada")
    return updated

async def delete_carrera(id: int):
    deleted = await Carrera.filter(id=id).delete()
    if deleted == 0:
        raise Exception("Carrera no encontrada")
    return deleted
