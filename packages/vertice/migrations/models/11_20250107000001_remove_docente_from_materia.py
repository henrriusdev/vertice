from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "materias" DROP COLUMN IF EXISTS "id_docente_id";
        ALTER TABLE "materias" DROP COLUMN IF EXISTS "horarios";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "materias" ADD "id_docente_id" INT REFERENCES "docentes" ("id") ON DELETE CASCADE;
        ALTER TABLE "materias" ADD "horarios" JSONB;"""