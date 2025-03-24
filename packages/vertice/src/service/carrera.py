from model.carrera import Carrera


async def get_carreras():
    carreras = await Carrera.all()
    return [c.to_dict() for c in carreras]

async def get_carrera(id: int):
    return await Carrera.get_or_none(id=id)

async def add_carrera(data):
    existe = await Carrera.get_or_none(id=data["id"])
    if existe:
        raise Exception("Carrera ya existe")
    return await Carrera.create(**data)

async def update_carrera(id: int, data):
    return await Carrera.filter(id=id).update(**data)

async def delete_carrera(id: int):
    return await Carrera.filter(id=id).delete()