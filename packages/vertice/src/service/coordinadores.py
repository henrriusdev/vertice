from src.model.coordinador import Coordinador
from src.model.usuario import Usuario
from src.model.carrera import Carrera
from tortoise.exceptions import DoesNotExist
from src.model.configuracion import Configuracion
from src.model.estudiante import Estudiante
from src.model.matricula import Matricula


async def get_coordinadores():
    try:
        coordinadores = await Coordinador.all().prefetch_related("usuario", "carrera").order_by("usuario__nombre")
        resultado = []
        for c in coordinadores:
            resultado.append({
                "id": c.id,
                "usuario": c.usuario.id,
                "cedula": c.usuario.cedula,
                "nombre": c.usuario.nombre,
                "correo": c.usuario.correo,
                "telefono": c.telefono,
                "carrera": c.carrera.nombre,
                "activo": c.usuario.activo
            })
        return resultado
    except Exception as ex:
        raise Exception(ex)


async def get_coordinador(id: int):
    try:
        c = await Coordinador.get(id=id).prefetch_related("usuario", "carrera")
        return {
            "id": c.id,
            "usuario": c.usuario.id,
            "cedula": c.usuario.cedula,
            "nombre": c.usuario.nombre,
            "correo": c.usuario.correo,
            "telefono": c.telefono,
            "carrera": c.carrera.nombre,
            "carrera_id": c.carrera.id
        }
    except DoesNotExist:
        return None
    except Exception as ex:
        raise Exception(ex)


async def get_coordinador_by_usuario(usuario_id: int):
    try:
        c = await Coordinador.get(usuario_id=usuario_id).prefetch_related("carrera")
        return c
    except DoesNotExist:
        return None
    except Exception as ex:
        raise Exception(ex)


async def add_coordinador(usuario_id: int, carrera_id: int, telefono: str):
    try:
        usuario = await Usuario.get(id=usuario_id)
        carrera = await Carrera.get(id=carrera_id)

        coordinador = Coordinador(usuario=usuario, carrera=carrera, telefono=telefono)
        await coordinador.save()
        return coordinador.id
    except Exception as ex:
        raise Exception(ex)


async def update_coordinador(id: int, carrera_id: int = None, telefono: str = None):
    try:
        coordinador = await Coordinador.get(id=id)

        if carrera_id:
            carrera = await Carrera.get(id=carrera_id)
            coordinador.carrera = carrera

        if telefono:
            coordinador.telefono = telefono

        await coordinador.save()
        return True
    except DoesNotExist:
        return False
    except Exception as ex:
        raise Exception(ex)


async def delete_coordinador(cedula: str):
    try:
        coordinador = await Coordinador.get(usuario__cedula=cedula)
        usuario = await coordinador.usuario
        usuario.activo = False
        await usuario.save()
        return True
    except DoesNotExist:
        return False
    except Exception as ex:
        raise Exception(ex)


async def toggle_coordinador_status(cedula: str):
    try:
        coordinador = await Coordinador.get(usuario__cedula=cedula)
        usuario = await coordinador.usuario
        usuario.activo = not usuario.activo
        await usuario.save()
        return True
    except DoesNotExist:
        return False
    except Exception as ex:
        raise Exception(ex)

