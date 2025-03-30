from src.model.usuario import Usuario
from src.service.estudiantes import validar_pagos_estudiante
from tortoise.exceptions import DoesNotExist, IntegrityError
from werkzeug.security import check_password_hash

async def login(correo: str, password: str):
    try:
        usuario = await Usuario.filter(correo=correo).prefetch_related("rol").first()
        print(f"Usuario encontrado: {usuario}")

        if not usuario or not check_password_hash(usuario.password, password):
            return None

        if usuario.rol.nombre.lower() == "estudiante":
            await validar_pagos_estudiante(usuario)

        return usuario

    except DoesNotExist:
        return None
    except Exception as ex:
        raise Exception(ex)


async def get_usuario_por_correo(correo: str, incluir: str = None):
    try:
        relations = ["rol"]

        incluir = (incluir or "").lower()

        if incluir == "estudiante":
            relations.append("estudiante")
        elif incluir == "docente":
            relations.append("docente")
        elif incluir == "coordinador":
            relations.append("coordinador")

        return await Usuario.get(correo=correo).prefetch_related(*relations)

    except Exception:
        return None


async def update_password(correo: str, new_password: str):
    try:
        usuario = await Usuario.get(correo=correo)
        usuario.password = new_password
        await usuario.save()
        return True
    except Exception as ex:
        raise Exception(ex)
    

async def update_email(correo: str, new_email: str):
    try:
        usuario = await Usuario.get(correo=correo)
        usuario.correo = new_email
        await usuario.save()
        return True
    except Exception as ex:
        raise Exception(ex)
    

async def registrar_usuario(usuario: Usuario):
    try:
        existente = await Usuario.filter(correo=usuario.correo).first()
        if existente:
            raise Exception("Ya existe un usuario con este correo")

        existente_cedula = await Usuario.filter(cedula=usuario.cedula).first()
        if existente_cedula:
            raise Exception("Ya existe un usuario con esta cédula")

        await usuario.save()
        return usuario

    except IntegrityError:
        raise Exception("Error al registrar usuario. Verifica los campos únicos.")
    except Exception as ex:
        raise ex
    

async def bloquear_usuario(correo: str):
    try:
        usuario = await Usuario.get(correo=correo)
        usuario.activo = False
        await usuario.save()
        return True
    except DoesNotExist:
        raise Exception("Usuario no encontrado")
    except Exception as ex:
        raise Exception(f"Error al bloquear usuario: {ex}")


async def reactivar_usuario(correo: str):
    try:
        usuario = await Usuario.get(correo=correo)
        usuario.activo = True
        await usuario.save()
        return True
    except DoesNotExist:
        raise Exception("Usuario no encontrado")
    except Exception as ex:
        raise Exception(f"Error al reactivar usuario: {ex}")