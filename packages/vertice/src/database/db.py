from tortoise import Tortoise
from src.model.rol import Rol
from src.model.usuario import Usuario
from src.model.metodo_pago import MetodoPago
from src.settings import settings
from werkzeug.security import generate_password_hash

async def init_db():
    DB_URL = f"postgres://{settings.PGSQL_USER}:{settings.PGSQL_PASSWORD}@{settings.PGSQL_HOST}:{settings.PGSQL_PORT}/{settings.PGSQL_DB}"
    
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["src.model"]},  # ajusta si tu módulo es diferente
    )
    
    # Roles por defecto
    roles = [
        "administrador",
        "caja",
        "control",
        "coordinacion",
        "estudiante",
        "docente",
    ]
    # Métodos de pago por defecto
    metodos = [
        "Transferencia bancaria",
        "Pago móvil",
        "Efectivo",
        "Divisas",
    ]
    hashed_password = generate_password_hash("admin123", method="pbkdf2:sha256")
    print("Inicializando DB...")

    # Roles
    for nombre in roles:
        obj, created = await Rol.get_or_create(nombre=nombre)
        print(f"Rol: {obj.nombre}, creado: {created}")

    # Métodos
    for nombre in metodos:
        obj, created = await MetodoPago.get_or_create(nombre=nombre)
        print(f"Metodo: {obj.nombre}, creado: {created}")

    # Superusuario
    print("Creando superusuario...")
    rol_super = await Rol.get(nombre="administrador")
    obj, created = await Usuario.get_or_create(
        correo="admin@admin.com",  # clave única real
        defaults={
            "cedula": "00000000",
            "nombre": "Admin",
            "password": hashed_password,
            "rol": rol_super,
        }
    )

    print(f"Usuario: {obj.correo}, creado: {created}")
