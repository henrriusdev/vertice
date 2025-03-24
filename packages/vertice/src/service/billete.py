# services/billetes_service.py
from model.billete import Billete

async def get_billetes():
    billetes = await Billete.all()
    return [b.to_dict() for b in billetes]

async def get_billete(id: int):
    billete = await Billete.get_or_none(id=id)
    if billete:
        return billete.to_dict()
    raise Exception("Billete no existe")

async def add_billete(data):
    return await Billete.create(**data)

async def update_billete(id: int, data):
    return await Billete.filter(id=id).update(**data)