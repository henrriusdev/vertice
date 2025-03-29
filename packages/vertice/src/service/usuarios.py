from model.usuario import Usuario
from service.estudiantes import validar_pagos_estudiante
from tortoise.exceptions import DoesNotExist, IntegrityError

async def login(correo: str, password: str):
    try:
        usuario = await Usuario.get(correo=correo).prefetch_related("rol")

        if not usuario or usuario.password != password:
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
        elif incluir == "superusuario":
            relations.append("superusuario")
        elif incluir == "control":
            relations.append("control")
        elif incluir == "coordinador":
            relations.append("coordinador")
        elif incluir == "caja":
            relations.append("caja")

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