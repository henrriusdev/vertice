from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Agregar campo orden
        ALTER TABLE "pregunta_seguridad" ADD "orden" INT NOT NULL DEFAULT 0;
        
        -- Crear índice único para usuario_id y orden
        CREATE UNIQUE INDEX "uid_pregunta_se_usuario__orden" ON "pregunta_seguridad" ("usuario_id", "orden");
        
        -- Actualizar descripción de la tabla
        COMMENT ON TABLE "pregunta_seguridad" IS 'Preguntas de seguridad del usuario';
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Eliminar índice único
        DROP INDEX "uid_pregunta_se_usuario__orden";
        
        -- Eliminar campo orden
        ALTER TABLE "pregunta_seguridad" DROP COLUMN "orden";
        
        -- Restaurar descripción de la tabla
        COMMENT ON TABLE "pregunta_seguridad" IS 'Pregunta de seguridad del usuario';
    """
