from model.factura import Factura
from tortoise.transactions import in_transaction

async def get_current_number():
    factura = await Factura.get()
    return factura.numero

async def increment_number():
    async with in_transaction():
        factura = await Factura.get()
        factura.numero += 1
        await factura.save()

async def get_incremented_number():
    await increment_number()
    return await get_current_number()