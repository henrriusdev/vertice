from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "docentes" DROP COLUMN "observaciones";
        ALTER TABLE "docentes" DROP COLUMN "dedicacion";
        ALTER TABLE "docentes" DROP COLUMN "estatus";
        ALTER TABLE "estudiantes" ADD "estatus" VARCHAR(20) NOT NULL DEFAULT 'Activo';
        ALTER TABLE "billetes" ADD CONSTRAINT "fk_billetes_pagos_1bf39b06" FOREIGN KEY ("pago_id") REFERENCES "pagos" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_billetes_pago_id_8903b8" ON "billetes" ("pago_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_billetes_pago_id_8903b8";
        ALTER TABLE "billetes" DROP CONSTRAINT IF EXISTS "fk_billetes_pagos_1bf39b06";
        ALTER TABLE "docentes" ADD "observaciones" TEXT;
        ALTER TABLE "docentes" ADD "dedicacion" VARCHAR(50);
        ALTER TABLE "docentes" ADD "estatus" VARCHAR(20) NOT NULL DEFAULT 'Activo';
        ALTER TABLE "estudiantes" DROP COLUMN "estatus";"""
