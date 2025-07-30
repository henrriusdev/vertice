from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "carreras" ADD "activo" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "coordinadores" ADD "activo" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "docentes" ADD "activo" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "estudiantes" ADD "activo" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "materias" ADD "activo" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "pagos" ADD "activo" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "peticiones" ADD "activo" BOOL NOT NULL DEFAULT True;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pagos" DROP COLUMN "activo";
        ALTER TABLE "carreras" DROP COLUMN "activo";
        ALTER TABLE "docentes" DROP COLUMN "activo";
        ALTER TABLE "materias" DROP COLUMN "activo";
        ALTER TABLE "peticiones" DROP COLUMN "activo";
        ALTER TABLE "estudiantes" DROP COLUMN "activo";
        ALTER TABLE "coordinadores" DROP COLUMN "activo";"""
