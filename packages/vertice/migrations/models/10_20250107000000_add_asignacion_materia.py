from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "asignacion_materia" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "horarios" JSONB NOT NULL,
    "nombre" VARCHAR(15) NOT NULL,
    "materia_id" VARCHAR(15) NOT NULL REFERENCES "materias" ("id") ON DELETE CASCADE,
    "profesor_id" INT NOT NULL REFERENCES "docentes" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "asignacion_materia" IS 'Asignación de Profesor y Horarios a Materia';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "asignacion_materia";"""