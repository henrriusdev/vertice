from datetime import datetime
from src.model.docente import Docente
from src.model.peticion import Peticion
from src.model.usuario import Usuario
from tortoise.exceptions import DoesNotExist

async def get_docentes():
    try:
        docentes = await Docente.all().prefetch_related("usuario")
        resultado = []
        for d in docentes:
            resultado.append({
                "id": d.id,
                "cedula": d.usuario.cedula,
                "nombre": d.usuario.nombre,
                "correo": d.usuario.correo,
                "usuario": d.usuario.id,
                "titulo": d.titulo,
                "dedicacion": d.dedicacion,
                "especialidad": d.especialidad,
                "estatus": d.estatus,
                "fecha_ingreso": format_fecha(d.fecha_ingreso) if d.fecha_ingreso else None,
                "observaciones": d.observaciones
            })
        return resultado
    except Exception as ex:
        raise Exception(ex)


async def get_docente(id: int):
    try:
        d = await Docente.get(id=id).prefetch_related("usuario")
        return {
            "id": d.id,
            "cedula": d.usuario.cedula,
            "nombre": d.usuario.nombre,
            "correo": d.usuario.correo,
            "titulo": d.titulo,
            "dedicacion": d.dedicacion,
            "especialidad": d.especialidad,
            "estatus": d.estatus,
            "fecha_ingreso": format_fecha(d.fecha_ingreso) if d.fecha_ingreso else None,
            "observaciones": d.observaciones
        }
    except DoesNotExist:
        return None
    except Exception as ex:
        raise Exception(ex)

def parse_fecha(fecha_str: str) -> datetime:
    return datetime.strptime(fecha_str, "%d/%m/%Y")

def format_fecha(fecha: datetime):
    return fecha.strftime("%d/%m/%Y")

async def add_docente(usuario_id: int, titulo: str, dedicacion: str, especialidad: str, estatus: str = "Activo", fecha_ingreso=None, observaciones=None):
    try:
        usuario = await Usuario.get(id=usuario_id)
        docente = Docente(
            usuario=usuario,
            titulo=titulo,
            dedicacion=dedicacion,
            especialidad=especialidad,
            estatus=estatus,
            fecha_ingreso=parse_fecha(fecha_ingreso) if fecha_ingreso else None,
            observaciones=observaciones
        )
        await docente.save()
        return docente.id
    except Exception as ex:
        raise Exception(ex)


async def update_docente(id: int, **kwargs):
    try:
        docente = await Docente.get(id=id)
        for key, value in kwargs.items():
            if key == "fecha_ingreso":
                if isinstance(value, str):
                    value = parse_fecha(value)
            elif hasattr(docente, key):
                setattr(docente, key, value)
        await docente.save()
        return True
    except DoesNotExist:
        return False
    except Exception as ex:
        raise Exception(ex)


async def delete_docente(cedula: str):
    try:
        docente = await Docente.get(usuario__cedula=cedula)
        await docente.delete()
        await docente.usuario.delete()
        return True
    except DoesNotExist:
        return False
    except Exception as ex:
        raise Exception(ex)


async def get_peticiones_por_docente(docente_cedula: str):
    try:
        peticiones = await Peticion.filter(id_docente__cedula=docente_cedula).prefetch_related(
            "id_materia", "id_estudiante"
        )

        resultado = []
        for p in peticiones:
            estudiante = p.id_estudiante
            materia = p.id_materia

            resultado.append({
                "id": p.id,
                "descripcion": p.descripcion,
                "estado": p.estado,
                "campo": p.campo,
                "estudiante": {
                    "cedula": estudiante.cedula,
                    "nombre": estudiante.fullname
                },
                "materia": {
                    "id": materia.id,
                    "nombre": materia.nombre
                }
            })

        return resultado

    except Exception as ex:
        raise Exception(ex)