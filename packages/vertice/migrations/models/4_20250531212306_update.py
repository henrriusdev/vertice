from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "pregunta_seguridad" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "pregunta" VARCHAR(255) NOT NULL,
    "respuesta" VARCHAR(255) NOT NULL,
    "fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "usuario_id" INT NOT NULL REFERENCES "usuarios" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "pregunta_seguridad" IS 'Pregunta de seguridad del usuario';
        ALTER TABLE "usuarios" ADD "pregunta_configurada" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "usuarios" DROP COLUMN "pregunta_configurada";
        DROP TABLE IF EXISTS "pregunta_seguridad";"""
