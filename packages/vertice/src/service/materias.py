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
        if materia["horarios"]:
            for horario in materia["horarios"]:
                horarios.append({
                    "dia": horario["dia"],
                    "hora_inicio": horario["hora_inicio"],
                    "hora_fin": horario["hora_fin"]
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


async def update_materia(materia: dict):
    try:
        m = await Materia.get_or_none(id=materia["id"])
        if not m:
            return 0

        horarios = []
        print(materia["horarios"])
        if materia["horarios"]:
            for horario in materia["horarios"]:
                horarios.append({
                    "dia": horario["dia"],
                    "hora_inicio": horario["hora_inicio"],
                    "hora_fin": horario["hora_fin"]
                })

        m.nombre = materia["nombre"]
        m.prelacion = materia["prelacion"]
        m.unidad_credito = materia["unidad_credito"]
        m.hp = materia["hp"]
        m.ht = materia["ht"]
        m.semestre = materia["semestre"]
        m.id_carrera_id = materia["id_carrera"]
        m.id_docente_id = materia["id_docente"]
        m.horarios = horarios
        m.modalidad = materia["modalidad"]
        m.maximo = materia["maximo"]

        await m.save()
        return 1
    except Exception as ex:
        raise Exception(ex)


async def get_materias_validas(cedula_estudiante: str):
    try:
        ciclo = (await Configuracion.get(id=1)).ciclo
        estudiante = await Estudiante.get(usuario__cedula=cedula_estudiante).prefetch_related("usuario", "carrera")

        ya_inscrito = await Matricula.filter(cedula_estudiante=estudiante, ciclo=ciclo).exists()
        if ya_inscrito:
            raise Exception("Usted ya tiene inscrito su horario, no puede inscribir más materias o modificarlo")

        materias_validas = []

        if estudiante.usuario.rol_id == 4 or estudiante.semestre == 1:
            materias = await Materia.filter(
                semestre=1,
                id_carrera=estudiante.carrera_id,
            ).exclude(id_docente=None).prefetch_related("id_carrera", "id_docente", "id_docente__usuario")
        else:
            materias = await Materia.filter(
                id_carrera=estudiante.carrera_id,
                semestre__lte=estudiante.semestre
            ).exclude(id_docente=None).prefetch_related("id_carrera", "id_docente", "id_docente__usuario")

        for materia in materias:
            # Evitar mostrar materias ya aprobadas
            matriculas = await Matricula.filter(cod_materia=materia, cedula_estudiante=estudiante.id)
            aprobada = any(sum(m.notas) > 9.5 for m in matriculas)
            if aprobada:
                continue

            # Verificar prelación si aplica
            if estudiante.semestre > 1 and materia.prelacion:
                prelaciones = await Matricula.filter(
                    cod_materia__id=materia.prelacion,
                    cedula_estudiante=estudiante.id
                )
                if not any(sum(m.notas) > 9.5 for m in prelaciones):
                    continue

            # Procesar horarios
            horarios = materia.horarios or []
            if isinstance(horarios, str):
                try:
                    horarios = json.loads(horarios)
                except json.JSONDecodeError:
                    horarios = []

            count = await Matricula.filter(cod_materia=materia, ciclo=ciclo).count()

            materias_validas.append({
                "id": materia.id,
                "nombre": materia.nombre,
                "prelacion": materia.prelacion,
                "unidad_credito": materia.unidad_credito,
                "hp": materia.hp,
                "ht": materia.ht,
                "semestre": materia.semestre,
                "id_carrera": materia.id_carrera_id,
                "id_docente": materia.id_docente_id,
                "modalidad": materia.modalidad,
                "maximo": materia.maximo,
                "horarios": horarios,
                "cantidad_estudiantes": count,
                "carrera": {
                    "id": materia.id_carrera.id,
                    "nombre": materia.id_carrera.nombre
                },
                "docente": {
                    "id": materia.id_docente.id,
                    "nombre": materia.id_docente.usuario.nombre,
                }
            })

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
                "nombre": usuario.nombre,
                "notas": notas,
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
        nombre_campo = int(nombre_campo) - 1
        notas[nombre_campo] = float(valor)
        matricula.notas = notas

        # Recalcular el promedio
        config = await Configuracion.get(id=1)
        porcentajes = config.porcentajes or [0, 0, 0]
        promedio = sum([
            float(notas[i]) * (float(porcentajes[i]) / 100) for i in range(min(len(notas), len(porcentajes)))
        ])
        matricula.promedio = round(promedio, 2)

        await matricula.save()
        return 1
    except Exception as ex:
        raise Exception(ex)
    

async def listar_materias_asignadas():
    try:
        ciclo = (await Configuracion.get(id=1)).ciclo

        materias_ids = await Matricula.filter(ciclo=ciclo).distinct().values_list("cod_materia_id", flat=True)

        materias = await Materia.filter(
            id__in=materias_ids
        ).exclude(id_docente=None).prefetch_related("id_carrera", "id_docente__usuario")

        resultado = {"contenido": {"materia": []}}

        for m in materias:
            horarios = m.horarios or []
            if isinstance(horarios, str):
                try:
                    horarios = json.loads(horarios)
                except json.JSONDecodeError:
                    horarios = []

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
                "horarios": horarios,
                "maximo": m.maximo,
                "modalidad": m.modalidad,
                "carrera": m.id_carrera.nombre if m.id_carrera else None,
                "docente": {
                    "cedula": usuario.cedula,
                    "nombre": usuario.nombre,
                    "titulo": docente.titulo,
                    "especialidad": docente.especialidad,
                    "dedicacion": docente.dedicacion,
                    "estatus": docente.estatus
                }
            })

        return resultado

    except Exception as ex:
        raise Exception(ex)


async def get_materia_con_nombre_y_config(materia_id: str, correo: str):
    try:
        materia = await Materia.get_or_none(id=materia_id, id_docente__usuario__correo=correo).prefetch_related("id_carrera")
        if not materia:
            return None

        config = await Configuracion.get(id=1)
        return {
            "id": materia.id,
            "nombre": materia.nombre,
            "num_cortes": len(config.porcentajes or []),
            "carrera": materia.id_carrera.nombre
        }
    except Exception as ex:
        raise Exception(ex)


async def get_estudiantes_con_notas(materia_id: str):
    try:
        config = await Configuracion.get(id=1)
        porcentajes = config.porcentajes or []

        matriculas = await Matricula.filter(cod_materia_id=materia_id).prefetch_related("cedula_estudiante__usuario")

        estudiantes = []
        for m in matriculas:
            usuario = m.cedula_estudiante.usuario
            notas = m.notas or [0] * len(porcentajes)

            promedio = sum([
                float(notas[i]) * (float(porcentajes[i]) / 100)
                for i in range(min(len(notas), len(porcentajes)))
            ])

            estudiantes.append({
                "nombre": usuario.nombre,
                "cedula": usuario.cedula,
                "notas": notas,
                "promedio": round(promedio, 2)
            })

        return estudiantes
    except Exception as ex:
        raise Exception(ex)
