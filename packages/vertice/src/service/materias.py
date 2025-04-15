import json
from src.model.materia import Materia
from src.model.configuracion import Configuracion
from src.model.matricula import Matricula
from src.model.estudiante import Estudiante

async def get_materias():
    try:
        materias = await Materia.all().prefetch_related("id_carrera")
        join = {"materias": []}

        for m in materias:
            # Forzar a dict para hacer serializable
            horarios = m.horarios
            if isinstance(horarios, str):
                try:
                    horarios = json.loads(horarios)
                except json.JSONDecodeError:
                    horarios = []

            join["materias"].append({
                "id": m.id,
                "nombre": m.nombre,
                "prelacion": m.prelacion,
                "unidad_credito": m.unidad_credito,
                "hp": m.hp,
                "ht": m.ht,
                "semestre": m.semestre,
                "id_carrera": m.id_carrera_id,  # usar el id directamente
                "modalidad": m.modalidad,
                "maximo": m.maximo,
                "id_docente": m.id_docente_id,
                "horarios": horarios
            })

        return join
    except Exception as ex:
        raise Exception(ex)


async def add_materia(materia: dict):
    try:
        existe = await Materia.filter(id=materia["id"]).exists()
        if existe:
            return "materia ya existe"

        horarios = []
        print(materia["horarios"])
        print("AAA")
        if materia["horarios"]:
            for horario in materia["horarios"]:
                horarios.append({
                    "dia": horario["dia"],
                    "hora_inicio": horario["inicio"],
                    "hora_fin": horario["fin"]
                })

        await Materia.create(
            id=materia["id"],
            nombre=materia["nombre"],
            prelacion=materia["prelacion"] if materia["prelacion"] else "",
            unidad_credito=materia["unidad_credito"],
            hp=materia["hp"],
            ht=materia["ht"],
            semestre=materia["semestre"],
            id_carrera_id=materia["id_carrera"],
            id_docente_id=materia["id_docente"],
            horarios=horarios,
            modalidad=materia["modalidad"],
            maximo=materia["maximo"]
        )

        return 1
    except Exception as ex:
        raise Exception(ex)


async def update_materia(materia):
    try:
        m = await Materia.get_or_none(id=materia.id)
        if not m:
            return 0

        horarios = []
        if materia.dia and materia.hora_inicio and materia.hora_fin:
            horarios.append({
                "dia": materia.dia,
                "hora_inicio": materia.hora_inicio,
                "hora_fin": materia.hora_fin
            })
        if materia.dia2 and materia.hora_inicio2 and materia.hora_fin2:
            horarios.append({
                "dia": materia.dia2,
                "hora_inicio": materia.hora_inicio2,
                "hora_fin": materia.hora_fin2
            })

        m.nombre = materia.nombre
        m.prelacion = materia.prelacion
        m.unidad_credito = materia.unidad_credito
        m.hp = materia.hp
        m.ht = materia.ht
        m.semestre = materia.semestre
        m.id_carrera_id = materia.id_carrera
        m.id_docente_id = materia.id_docente
        m.horarios = horarios
        m.ciclo = materia.ciclo
        m.modalidad = materia.modalidad
        m.maximo = materia.maximo

        await m.save()
        return 1
    except Exception as ex:
        raise Exception(ex)


async def get_materias_validas(cedula_estudiante: str):
    try:
        ciclo = (await Configuracion.get(id=1)).ciclo
        estudiante = await Estudiante.get(usuario__cedula=cedula_estudiante).prefetch_related("usuario", "carrera")

        # Validar si ya tiene materias inscritas en el ciclo
        ya_inscrito = await Matricula.filter(cedula_estudiante=estudiante.id, ciclo=ciclo).exists()
        if ya_inscrito:
            raise Exception("Usted ya tiene inscrito su horario, no puede inscribir más materias o modificarlo")

        materias_validas = []

        # Materias para nuevo ingreso
        if estudiante.usuario.rol_id == 4 or estudiante.semestre == 1:
            materias = await Materia.filter(
                semestre=1,
                id_carrera=estudiante.carrera_id,
                ciclo=ciclo
            ).exclude(id_docente=None)
        else:
            materias = await Materia.filter(
                id_carrera=estudiante.carrera_id,
                ciclo=ciclo
            ).exclude(id_docente=None)

        for materia in materias:
            # Validar prelación si aplica
            if estudiante.semestre > 1 and materia.prelacion:
                aprobada = await Matricula.filter(
                    cod_materia__id=materia.prelacion,
                    cedula_estudiante=estudiante.id
                ).filter(notas__0__gte=50).exists()

                if not aprobada:
                    continue

            horarios = materia.horarios or []

            # Si por error se guardó como string
            if isinstance(horarios, str):
                try:
                    horarios = json.loads(horarios)
                except json.JSONDecodeError:
                    horarios = []

            materia.dia = horarios[0]["dia"] if len(horarios) > 0 else None
            materia.hora_inicio = horarios[0]["hora_inicio"] if len(horarios) > 0 else None
            materia.hora_fin = horarios[0]["hora_fin"] if len(horarios) > 0 else None
            materia.dia2 = horarios[1]["dia"] if len(horarios) > 1 else None
            materia.hora_inicio2 = horarios[1]["hora_inicio"] if len(horarios) > 1 else None
            materia.hora_fin2 = horarios[1]["hora_fin"] if len(horarios) > 1 else None

            count = await Matricula.filter(cod_materia=materia, ciclo=ciclo).count()
            materia.cantidad_estudiantes = count

            materias_validas.append(materia)

        return materias_validas

    except Exception as ex:
        raise Exception(ex)


async def get_materia(id: str):
    try:
        config = await Configuracion.get(id=1)
        materia = await Materia.get(id=id).prefetch_related("id_carrera")
        join = {
            "ciclo": config.ciclo,
            "materia": {
                "id": materia.id,
                "nombre": materia.nombre,
                "estudiantes": [],
                "carrera": materia.id_carrera.nombre
            }
        }

        matriculas = await Matricula.filter(cod_materia=materia).prefetch_related("cedula_estudiante__usuario")

        for m in matriculas:
            estudiante = await m.cedula_estudiante
            usuario = await estudiante.usuario

            notas = m.notas or [0, 0, 0]
            porcentajes = config.porcentajes or [0, 0, 0]

            promedio = sum([
                notas[i] * (porcentajes[i] / 100) for i in range(min(len(notas), len(porcentajes)))
            ])

            join["materia"]["estudiantes"].append({
                "cedula": usuario.cedula,
                "nombre": usuario.fullname,
                "nota1": notas[0],
                "nota2": notas[1],
                "nota3": notas[2],
                "promedio": round(promedio, 2)
            })

        return join

    except Exception as ex:
        raise Exception(ex)


async def delete_materia(materia):
    try:
        eliminado = await Materia.filter(id=materia.id).delete()
        return eliminado[0]  # cantidad de filas eliminadas
    except Exception as ex:
        raise Exception(ex)


async def modificar_materia_estudiante(cod_materia, cedula_estudiante, nombre_campo, valor):
    try:
        # Obtener la matrícula
        matricula = await Matricula.get(
            cod_materia_id=cod_materia,
            cedula_estudiante__usuario__cedula=cedula_estudiante
        )

        # Actualizar el campo específico dentro de "notas"
        notas = matricula.notas or [0, 0, 0]
        index = {"nota1": 0, "nota2": 1, "nota3": 2}.get(nombre_campo)
        if index is None:
            raise Exception("Campo no válido")

        notas[index] = valor
        matricula.notas = notas

        # Recalcular el promedio
        config = await Configuracion.get(id=1)
        porcentajes = config.porcentajes or [0, 0, 0]
        promedio = sum([
            notas[i] * (porcentajes[i] / 100) for i in range(min(len(notas), len(porcentajes)))
        ])
        matricula.promedio = round(promedio, 2)

        await matricula.save()
        return 1
    except Exception as ex:
        raise Exception(ex)
    

async def listar_materias_asignadas():
    try:
        ciclo = (await Configuracion.get(id=1)).ciclo

        # Obtener IDs de materias con matrícula en ese ciclo
        materias_ids = await Matricula.filter(ciclo=ciclo).distinct().values_list("cod_materia_id", flat=True)

        materias = await Materia.filter(
            id__in=materias_ids
        ).exclude(id_docente=None).prefetch_related("id_carrera", "id_docente__usuario")

        resultado = {"contenido": {"materia": []}}

        for m in materias:
            horarios = m.horarios or []
            dia = horarios[0]["dia"] if len(horarios) > 0 else None
            hora_inicio = horarios[0]["hora_inicio"] if len(horarios) > 0 else None
            hora_fin = horarios[0]["hora_fin"] if len(horarios) > 0 else None
            dia2 = horarios[1]["dia"] if len(horarios) > 1 else None
            hora_inicio2 = horarios[1]["hora_inicio"] if len(horarios) > 1 else None
            hora_fin2 = horarios[1]["hora_fin"] if len(horarios) > 1 else None

            docente = m.id_docente
            usuario = docente.usuario

            resultado["contenido"]["materia"].append({
                "id": m.id,
                "nombre": m.nombre,
                "prelacion": m.prelacion,
                "unidad_credito": m.unidad_credito,
                "hp": m.hp,
                "ht": m.ht,
                "semestre": m.semestre,
                "id_carrera": m.id_carrera_id,
                "id_docente": m.id_docente_id,
                "dia": dia,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "dia2": dia2,
                "hora_inicio2": hora_inicio2,
                "hora_fin2": hora_fin2,
                "maximo": m.maximo,
                "modalidad": m.modalidad,
                "carrera": m.id_carrera.nombre if m.id_carrera else None,
                "docente": {
                    "cedula": usuario.cedula,
                    "nombre": usuario.fullname,
                    "titulo": docente.titulo,
                    "especialidad": docente.especialidad,
                    "dedicacion": docente.dedicacion,
                    "estatus": docente.estatus
                }
            })

        return resultado

    except Exception as ex:
        raise Exception(ex)
