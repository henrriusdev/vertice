from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "billetes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "serial" VARCHAR(100) NOT NULL,
    "monto" DECIMAL(10,2) NOT NULL,
    "pago_id" INT NOT NULL
);
COMMENT ON TABLE "billetes" IS 'Billete';
CREATE TABLE IF NOT EXISTS "carreras" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nombre" VARCHAR(255) NOT NULL
);
COMMENT ON TABLE "carreras" IS 'Carrera';
CREATE TABLE IF NOT EXISTS "configuraciones" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "ciclo" VARCHAR(10) NOT NULL,
    "num_porcentaje" INT NOT NULL DEFAULT 3,
    "num_cuotas" INT NOT NULL DEFAULT 5,
    "horario_inicio" TIMESTAMPTZ NOT NULL,
    "horario_fin" TIMESTAMPTZ NOT NULL,
    "cuotas" JSONB,
    "porcentajes" JSONB
);
COMMENT ON TABLE "configuraciones" IS 'Configuración';
CREATE TABLE IF NOT EXISTS "metodos_pago" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nombre" VARCHAR(50) NOT NULL UNIQUE
);
COMMENT ON TABLE "metodos_pago" IS 'Metodo de pago';
CREATE TABLE IF NOT EXISTS "roles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nombre" VARCHAR(50) NOT NULL UNIQUE
);
COMMENT ON TABLE "roles" IS 'Rol';
CREATE TABLE IF NOT EXISTS "usuarios" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cedula" VARCHAR(20) NOT NULL UNIQUE,
    "nombre" VARCHAR(255) NOT NULL,
    "correo" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "activo" BOOL NOT NULL DEFAULT True,
    "ruta_foto" VARCHAR(255),
    "fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ultima_sesion" TIMESTAMPTZ,
    "rol_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "usuarios" IS 'Usuarios registrados en el sistema';
CREATE TABLE IF NOT EXISTS "coordinadores" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telefono" VARCHAR(20) NOT NULL,
    "carrera_id" INT NOT NULL REFERENCES "carreras" ("id") ON DELETE CASCADE,
    "usuario_id" INT NOT NULL UNIQUE REFERENCES "usuarios" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "coordinadores" IS 'Coordinación';
CREATE TABLE IF NOT EXISTS "docentes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "titulo" VARCHAR(50),
    "dedicacion" VARCHAR(50),
    "especialidad" VARCHAR(100),
    "estatus" VARCHAR(20) NOT NULL DEFAULT 'Activo',
    "fecha_ingreso" DATE,
    "observaciones" TEXT,
    "usuario_id" INT NOT NULL UNIQUE REFERENCES "usuarios" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "docentes" IS 'Docente';
CREATE TABLE IF NOT EXISTS "estudiantes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "semestre" INT NOT NULL,
    "promedio" DECIMAL(10,2) NOT NULL,
    "direccion" VARCHAR(300) NOT NULL,
    "fecha_nac" TIMESTAMPTZ NOT NULL,
    "edad" INT NOT NULL,
    "sexo" VARCHAR(20) NOT NULL,
    "carrera_id" INT NOT NULL REFERENCES "carreras" ("id") ON DELETE CASCADE,
    "usuario_id" INT NOT NULL UNIQUE REFERENCES "usuarios" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "estudiantes" IS 'Estudiante';
CREATE TABLE IF NOT EXISTS "materias" (
    "id" VARCHAR(15) NOT NULL PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "prelacion" VARCHAR(250) NOT NULL,
    "unidad_credito" INT NOT NULL,
    "hp" INT NOT NULL,
    "ht" INT NOT NULL,
    "semestre" INT NOT NULL,
    "horarios" JSONB,
    "modalidad" VARCHAR(20),
    "maximo" INT,
    "id_carrera_id" INT NOT NULL REFERENCES "carreras" ("id") ON DELETE CASCADE,
    "id_docente_id" INT REFERENCES "usuarios" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "materias" IS 'Materia';
CREATE TABLE IF NOT EXISTS "matriculas" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "notas" JSONB NOT NULL,
    "uc" INT NOT NULL,
    "ciclo" VARCHAR(10) NOT NULL,
    "cedula_estudiante_id" INT NOT NULL REFERENCES "estudiantes" ("id") ON DELETE CASCADE,
    "cod_materia_id" VARCHAR(15) NOT NULL REFERENCES "materias" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_matriculas_cod_mat_4288c0" UNIQUE ("cod_materia_id", "cedula_estudiante_id", "ciclo")
);
COMMENT ON TABLE "matriculas" IS 'Matricula';
CREATE TABLE IF NOT EXISTS "pagos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "monto" DECIMAL(12,2) NOT NULL,
    "concepto" VARCHAR(100) NOT NULL,
    "fecha_pago" TIMESTAMPTZ NOT NULL,
    "referencia_transferencia" VARCHAR(50),
    "ciclo" VARCHAR(10) NOT NULL,
    "tasa_divisa" DECIMAL(12,2),
    "cedula_estudiante_id" INT NOT NULL REFERENCES "estudiantes" ("id") ON DELETE CASCADE,
    "metodo_pago_id" INT NOT NULL REFERENCES "metodos_pago" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "pagos" IS 'Monto';
CREATE TABLE IF NOT EXISTS "peticiones" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "descripcion" VARCHAR(500) NOT NULL,
    "estado" VARCHAR(150) NOT NULL,
    "campo" VARCHAR(10) NOT NULL,
    "id_docente_id" INT NOT NULL REFERENCES "usuarios" ("id") ON DELETE CASCADE,
    "id_estudiante_id" INT NOT NULL REFERENCES "usuarios" ("id") ON DELETE CASCADE,
    "id_materia_id" VARCHAR(15) NOT NULL REFERENCES "materias" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "peticiones" IS 'Peticiones';
CREATE TABLE IF NOT EXISTS "sesiones_activas" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "jti" VARCHAR(255) NOT NULL UNIQUE,
    "creado_en" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "usuario_id" INT NOT NULL REFERENCES "usuarios" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "sesiones_activas" IS 'Sesiones activas por usuario';
CREATE TABLE IF NOT EXISTS "trazabilidad" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "accion" VARCHAR(300) NOT NULL,
    "fecha" TIMESTAMPTZ NOT NULL,
    "modulo" VARCHAR(50) NOT NULL,
    "nivel_alerta" INT,
    "usuario_id" INT NOT NULL REFERENCES "usuarios" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "trazabilidad" IS 'Trazabilidad';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
