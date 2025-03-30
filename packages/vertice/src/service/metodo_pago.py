from src.model.metodo_pago import MetodoPago

async def get_metodos():
    metodos = await MetodoPago.all()
    return [m.to_dict() for m in metodos]

async def get_metodo(id: int):
    return await MetodoPago.get_or_none(id=id)

async def add_metodo(data):
    metodo = await MetodoPago.create(**data)
    return metodo.id

async def update_metodo(id: int, data):
    return await MetodoPago.filter(id=id).update(**data)