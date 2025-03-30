from src.model.sesion_activa import SesionActiva
from src.model.usuario import Usuario
from datetime import datetime
from tortoise.exceptions import DoesNotExist

async def registrar_sesion(correo: str, jti: str):
    return await SesionActiva.create(correo=correo, jti=jti, creado_en=datetime.now())

async def eliminar_sesion(jti: str):
    return await SesionActiva.filter(jti=jti).delete()

async def eliminar_sesiones_usuario(correo: str):
    return await SesionActiva.filter(correo=correo).delete()

async def obtener_sesiones_usuario(correo: str):
    return await SesionActiva.filter(correo=correo).all()

async def verificar_sesion_activa(jti: str):
    return await SesionActiva.filter(jti=jti).exists()

async def registrar_sesion(correo: str, jti: str):
    try:
        usuario = await Usuario.get(correo=correo)
        # Eliminar sesiones anteriores (solo una sesión activa permitida)
        await SesionActiva.filter(usuario=usuario).delete()
        return await SesionActiva.create(usuario=usuario, jti=jti)
    except DoesNotExist:
        raise Exception("Usuario no encontrado")


async def eliminar_sesion_por_jti(jti: str):
    eliminado = await SesionActiva.filter(jti=jti).delete()
    return eliminado > 0


async def validar_sesion_activa(correo: str, jti: str):
    try:
        usuario = await Usuario.get(correo=correo)
        sesion = await SesionActiva.get(usuario=usuario, jti=jti)
        return sesion is not None
    except DoesNotExist:
        return False
