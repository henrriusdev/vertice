from tortoise import Tortoise
from src.settings import settings

async def init_db():
    DB_URL = f"postgres://{settings.PGSQL_USER}:{settings.PGSQL_PASSWORD}@{settings.PGSQL_HOST}:{settings.PGSQL_PORT}/{settings.PGSQL_DB}"
    
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["src.model"]},  # ajusta si tu módulo es diferente
    )
    # Si no quieres generar schemas automáticamente, no llames a generate_schemas()
    # await Tortoise.generate_schemas()
