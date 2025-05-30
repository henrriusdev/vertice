from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "usuarios" DROP COLUMN "ruta_foto";
        ALTER TABLE "usuarios" DROP COLUMN "ultima_sesion";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "usuarios" ADD "ruta_foto" VARCHAR(255);
        ALTER TABLE "usuarios" ADD "ultima_sesion" TIMESTAMPTZ;"""
