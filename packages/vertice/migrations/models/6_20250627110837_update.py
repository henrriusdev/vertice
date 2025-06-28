from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "docentes" DROP COLUMN "especialidad";
        ALTER TABLE "materias" DROP COLUMN "modalidad";
        DROP TABLE IF EXISTS "sesiones_activas";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "docentes" ADD "especialidad" VARCHAR(100);
        ALTER TABLE "materias" ADD "modalidad" VARCHAR(20);"""
