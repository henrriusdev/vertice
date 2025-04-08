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


async def get_usuarios():
    try:
        # get only users with rol superusuario and control
        data = await Usuario.filter(rol__nombre__in=["control", "caja"]).prefetch_related("rol").all()
        response = [u.to_dict() for u in data]
        return response
    except Exception as ex:
        raise Exception(ex)

async def get_usuario(id: int):
    try:
        usuario = await Usuario.filter(id=id).first()
        return usuario;
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
    
    
async def update_usuario(id: int, payload: dict):
    try:
        await Usuario.filter(id=id).update(**payload)
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
        usuario = await Usuario.get(id=usuario.id).select_related("rol")
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
    

async def delete_usuario(cedula: str):
    try:
        await Usuario.filter(cedula=cedula).delete()
        return True
    except DoesNotExist:
        raise Exception("Usuario no encontrado")
    except Exception as ex:
        raise Exception(f"Error al eliminar usuario: {ex}")
    