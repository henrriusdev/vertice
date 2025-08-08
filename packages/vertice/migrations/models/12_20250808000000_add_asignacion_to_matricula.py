from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "matriculas" ADD "asignacion_id" INT REFERENCES "asignacion_materia" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "matriculas" DROP COLUMN IF EXISTS "asignacion_id";"""