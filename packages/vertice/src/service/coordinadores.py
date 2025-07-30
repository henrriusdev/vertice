from src.model.coordinador import Coordinador
from src.model.usuario import Usuario
from src.model.carrera import Carrera
from tortoise.exceptions import DoesNotExist
from src.model.configuracion import Configuracion
from src.model.estudiante import Estudiante
from src.model.matricula import Matricula


async def get_coordinadores():
    try:
        coordinadores = await Coordinador.filter(usuario__activo=True).all().prefetch_related("usuario", "carrera").order_by("usuario__nombre")
        resultado = []
        for c in coordinadores:
            resultado.append({
                "id": c.id,
                "usuario": c.usuario.id,
                "cedula": c.usuario.cedula,
                "nombre": c.usuario.nombre,
                "correo": c.usuario.correo,
                "telefono": c.telefono,
                "carrera": c.carrera.nombre
            })
        return resultado
    except Exception as ex:
        raise Exception(ex)


async def get_coordinador(id: int):
    try:
        c = await Coordinador.filter(usuario__activo=True).get(id=id).prefetch_related("usuario", "carrera")
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
        c = await Coordinador.filter(usuario__activo=True).get(usuario_id=usuario_id).prefetch_related("carrera")
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


async def calcular_promedio_ponderado_estudiante(cedula: str):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula).prefetch_related("usuario")
        config = await Configuracion.get(id=1)
        porcentajes = config.porcentajes or []

        matriculas = await Matricula.filter(cedula_estudiante=estudiante).prefetch_related("cod_materia")
        total_uc = 0
        total_ponderado = 0

        for m in matriculas:
            notas = m.notas or []
            uc = m.uc or m.cod_materia.unidad_credito

            if not notas or len(notas) != len(porcentajes):
                continue  # Saltar si datos incompletos

            promedio = sum(n * (p / 100) for n, p in zip(notas, porcentajes))
            total_ponderado += promedio * uc
            total_uc += uc

        promedio_final = round(total_ponderado / total_uc, 2) if total_uc else 0

        estudiante.promedio = promedio_final
        await estudiante.save()

        return promedio_final

    except Exception as ex:
        raise Exception(ex)