from src.model.usuario import Usuario
from src.model.peticion import Peticion
from src.service.materias import modificar_materia_estudiante


async def get_peticiones():
    try:
        result = []

        peticiones = await Peticion.all().prefetch_related(
            "id_docente", "id_docente__rol",
            "id_estudiante",
            "id_materia"
        )

        for p in peticiones:
            peticion_data = {
                "id": p.id,
                "descripcion": p.descripcion,
                "estado": p.estado,
                "id_docente": p.id_docente_id,
                "id_estudiante": p.id_estudiante_id,
                "id_materia": p.id_materia_id,
                "campo": p.campo,
                "valor": p.valor,
            }

            result.append({
                "estudiante": {
                    "cedula": p.id_estudiante.cedula,
                    "nombre": p.id_estudiante.nombre
                },
                "docente": {
                    "cedula": p.id_docente.cedula,
                    "nombre": p.id_docente.nombre
                },
                "materia": {
                    "id": p.id_materia.id,
                    "nombre": p.id_materia.nombre
                },
                "peticion": peticion_data
            })

        return result

    except Exception as ex:
        raise Exception(ex)

async def get_peticion(id: int):
    try:
        p = await Peticion.get(id=id)
        return {
            "id": p.id,
            "descripcion": p.descripcion,
            "estado": p.estado,
            "id_docente": p.id_docente_id,
            "id_estudiante": p.id_estudiante_id,
            "id_materia": p.id_materia_id,
            "campo": p.campo,
            "valor": p.valor,
        }
    except Exception as ex:
        raise Exception(ex)


async def get_peticiones_pendientes():
    try:
        peticiones = await Peticion.filter(estado="Pendiente")
        return [p.__dict__ for p in peticiones]
    except Exception as ex:
        raise Exception(ex)


async def add_peticion(peticion: dict):
    try:
        estudiante = await Usuario.get(cedula=peticion["id_estudiante"])

        nueva = await Peticion.create(
            id_docente_id=peticion["id_docente"],
            descripcion=peticion["descripcion"],
            estado=peticion["estado"],
            id_estudiante=estudiante,
            id_materia_id=peticion["id_materia"],
            valor=peticion["valor"],
            campo=peticion["campo"]
        )
        return 1 if nueva else 0
    except Exception as ex:
        raise Exception(ex)


async def update_peticion(peticion: dict):
    try:
        p = await Peticion.get(id=peticion["id"]).prefetch_related("id_estudiante", "id_docente")
        if peticion["estado"]:
            p.estado = peticion["estado"]

        await p.save()

        if peticion["estado"] == "Aprobado":
            await modificar_materia_estudiante(p.id_materia_id, p.id_estudiante.cedula, p.campo, p.valor)

        return 1
    except Exception as ex:
        raise Exception(ex)


async def delete_peticion(peticion):
    try:
        pet = await Peticion.get(id=peticion["id"])
        pet.activo = False
        await pet.save()
        return 1
    except Exception as ex:
        raise Exception(ex)
