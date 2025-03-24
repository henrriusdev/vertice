from tortoise.contrib.flask import register_tortoise
from settings import settings

def init_db(app):
    DB_URL = f"postgres://{settings.PGSQL_USER}:{settings.PGSQL_PASSWORD}@{settings.PGSQL_HOST}:{settings.PGSQL_PORT}/{settings.PGSQL_DB}"

    register_tortoise(
        app,
        db_url=DB_URL,
        modules={'models': ['src.models']},
        generate_schemas=False,
        add_exception_handlers=True,
    )
