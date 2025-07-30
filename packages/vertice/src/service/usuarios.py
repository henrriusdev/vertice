from tortoise.exceptions import DoesNotExist, IntegrityError
from werkzeug.security import check_password_hash

from src.service.estudiantes import validar_pagos_estudiante
from src.model.usuario import Usuario
import time


async def login(correo: str, password: str):
    try:
        # First check if user exists with this email
        usuario = await Usuario.filter(correo=correo).prefetch_related("rol").first()
        
        if not usuario:
            return {"error": "EMAIL_NOT_FOUND", "message": "El correo electrónico no está registrado"}
            
        # Then check if user is active
        if not usuario.activo:
            return {"error": "ACCOUNT_INACTIVE", "message": "Esta cuenta ha sido desactivada"}
            
        # Finally check password
        if not check_password_hash(usuario.password, password):
            return {"error": "INVALID_PASSWORD", "message": "La contraseña es incorrecta"}

        if usuario.rol.nombre.lower() == "estudiante":
            await validar_pagos_estudiante(usuario)

        return usuario

    except DoesNotExist:
        return None
    except Exception as ex:
        raise Exception(ex)


# Simple in-memory cache with expiration time
_usuarios_cache = {"data": None, "timestamp": 0, "ttl": 60}  # 60 seconds TTL

async def get_usuarios():
    try:
        current_time = time.time()
        
        if _usuarios_cache["data"] is not None and (current_time - _usuarios_cache["timestamp"] < _usuarios_cache["ttl"]):
            return _usuarios_cache["data"]
            
        data = await Usuario.filter(rol__nombre__in=["control", "caja"]).select_related("rol").order_by("nombre")
        
        response = []
        for u in data:
            cedula_clean = u.cedula.replace("V-", "").replace("E-", "")
            
            response.append({
                "id": u.id,
                "cedula": u.cedula,
                "nombre": u.nombre,
                "correo": u.correo,
                "activo": u.activo,
                "fecha_creacion": u.fecha_creacion.strftime("%d/%m/%Y") if u.fecha_creacion else None,
                "cambiar_clave": u.check_password(cedula_clean),
                "pregunta_configurada": u.pregunta_configurada,
                "rol": {
                    "id": u.rol.id,
                    "nombre": u.rol.nombre,
                },
            })
        
        _usuarios_cache["data"] = response
        _usuarios_cache["timestamp"] = current_time
        
        return response
    except Exception as ex:
        raise Exception(ex)

async def get_usuario(id: int):
    try:
        usuario = await Usuario.filter(id=id).first()
        return usuario
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
        usuario = await Usuario.get(cedula=cedula)
        usuario.activo = False
        await usuario.save()
        return True
    except DoesNotExist:
        raise Exception("Usuario no encontrado")
    except Exception as ex:
        raise Exception(f"Error al eliminar usuario: {ex}")
