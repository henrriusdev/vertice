from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "docentes" DROP COLUMN "especialidad";
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "docentes" ADD "especialidad" VARCHAR(100);
    """
