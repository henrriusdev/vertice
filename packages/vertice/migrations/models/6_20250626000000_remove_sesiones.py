from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "sesiones_activas";
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "sesiones_activas" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "jti" VARCHAR(255) NOT NULL UNIQUE,
            "creado_en" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "usuario_id" INT NOT NULL REFERENCES "usuarios" ("id") ON DELETE CASCADE
        );
        COMMENT ON TABLE "sesiones_activas" IS 'Sesiones activas por usuario';
    """
