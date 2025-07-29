from src.utils.fecha import format_fecha, parse_fecha
from src.model.materia import Materia
from src.model.docente import Docente
from src.model.peticion import Peticion
from src.model.usuario import Usuario
from tortoise.exceptions import DoesNotExist

async def get_docentes():
    try:
        docentes = await Docente.all().prefetch_related("usuario").order_by("usuario__fecha_creacion")
        resultado = []
        for d in docentes:
            resultado.append({
                "id": d.id,
                "cedula": d.usuario.cedula,
                "nombre": d.usuario.nombre,
                "correo": d.usuario.correo,
                "usuario": d.usuario.id,
                "titulo": d.titulo,
                "fecha_ingreso": format_fecha(d.fecha_ingreso) if d.fecha_ingreso else None,
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
            "fecha_ingreso": format_fecha(d.fecha_ingreso) if d.fecha_ingreso else None,
        }
    except DoesNotExist:
        return None
    except Exception as ex:
        raise Exception(ex)

async def add_docente(usuario_id: int, titulo: str, fecha_ingreso=None):
    try:
        usuario = await Usuario.get(id=usuario_id)
        docente = Docente(
            usuario=usuario,
            titulo=titulo,
            fecha_ingreso=parse_fecha(fecha_ingreso) if fecha_ingreso else None,
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
                    "nombre": estudiante.nombre
                },
                "materia": {
                    "id": materia.id,
                    "nombre": materia.nombre
                }
            })

        return resultado

    except Exception as ex:
        raise Exception(ex)
    

async def obtener_materias_por_email_docente(email: str):
    try:
        usuario = await Usuario.get(correo=email).prefetch_related("docente")
        docente = await usuario.docente
        materias = await Materia.filter(id_docente=docente.id).prefetch_related("id_carrera")

        resultado = []
        for materia in materias:
            horarios = materia.horarios or []
            for horario in horarios:
                resultado.append({
                    "id": materia.id,
                    "nombre": materia.nombre,
                    "dia": horario.get("dia"),
                    "hora_inicio": horario.get("hora_inicio"),
                    "hora_fin": horario.get("hora_fin"),
                    "color": None,
                    "conflicto": False
                })
            
        return resultado
    except Exception as ex:
        raise Exception(ex)
