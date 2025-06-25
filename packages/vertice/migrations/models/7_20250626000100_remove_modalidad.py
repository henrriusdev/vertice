from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "materias" DROP COLUMN IF EXISTS "modalidad";
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "materias" ADD "modalidad" VARCHAR(20);
    """
