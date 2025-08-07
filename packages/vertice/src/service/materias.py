import json
from src.model.materia import Materia
from src.model.asignacion_materia import AsignacionMateria
from src.model.configuracion import Configuracion
from src.model.matricula import Matricula
from src.model.estudiante import Estudiante

async def get_materias(carrera_id=None):
    try:
        if carrera_id is not None:
            materias = await Materia.filter(id_carrera_id=carrera_id).prefetch_related("id_carrera")
        else:
            materias = await Materia.all().prefetch_related("id_carrera")
        join = {"materias": []}

        for m in materias:
            # Get asignaciones for this materia
            asignaciones = await AsignacionMateria.filter(materia_id=m.id).prefetch_related("profesor__usuario")
            
            asignaciones_data = []
            for asig in asignaciones:
                # Forzar a dict para hacer serializable
                horarios = asig.horarios
                if isinstance(horarios, str):
                    try:
                        horarios = json.loads(horarios)
                    except json.JSONDecodeError:
                        horarios = []

                asignaciones_data.append({
                    "id": asig.id,
                    "nombre": asig.nombre,
                    "horarios": horarios,
                    "profesor": {
                        "id": asig.profesor.id,
                        "nombre": asig.profesor.usuario.nombre
                    } if asig.profesor and asig.profesor.usuario else None
                })

            join["materias"].append({
                "id": m.id,
                "nombre": m.nombre,
                "prelacion": m.prelacion,
                "unidad_credito": m.unidad_credito,
                "hp": m.hp,
                "ht": m.ht,
                "semestre": m.semestre,
                "id_carrera": m.id_carrera_id,  # usar el id directamente
                "maximo": m.maximo,
                "activo": m.activo if hasattr(m, 'activo') else True,
                "asignaciones": asignaciones_data
            })

        return join
    except Exception as ex:
        raise Exception(ex)


async def add_materia(materia: dict):
    try:
        # Validate required fields
        if not materia.get("id"):
            raise ValueError("El código de la materia es requerido")
        if not materia.get("nombre"):
            raise ValueError("El nombre de la materia es requerido")
        if not materia.get("id_carrera"):
            raise ValueError("La carrera es requerida")

        existe = await Materia.filter(id=materia["id"]).exists()
        if existe:
            return "materia ya existe"

        # Set default values for numeric fields
        defaults = {
            "unidad_credito": 0,
            "hp": 0,
            "ht": 0,
            "semestre": 1,
            "maximo": 30
        }

        # Safe conversion to integers with defaults
        def safe_int(value, default):
            if not value and value != 0:
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        
        # Create materia with safe conversions
        nueva_materia = await Materia.create(
            id=str(materia["id"]),
            nombre=str(materia["nombre"]),
            prelacion=str(materia.get("prelacion", "")),
            unidad_credito=safe_int(materia.get("unidad_credito"), defaults["unidad_credito"]),
            hp=safe_int(materia.get("hp"), defaults["hp"]),
            ht=safe_int(materia.get("ht"), defaults["ht"]),
            semestre=safe_int(materia.get("semestre"), defaults["semestre"]),
            id_carrera_id=str(materia["id_carrera"]),
            maximo=safe_int(materia.get("maximo"), defaults["maximo"])
        )

        # Handle asignaciones if provided
        if materia.get("asignaciones"):
            for asignacion in materia["asignaciones"]:
                horarios = []
                if asignacion.get("horarios"):
                    for horario in asignacion["horarios"]:
                        horarios.append({
                            "dia": horario["dia"],
                            "hora_inicio": horario["hora_inicio"],
                            "hora_fin": horario["hora_fin"]
                        })

                await AsignacionMateria.create(
                    materia=nueva_materia,
                    profesor_id=asignacion.get("profesor_id"),
                    horarios=horarios,
                    nombre=asignacion.get("nombre", "")
                )

        return 1
    except ValueError as ve:
        raise Exception(str(ve))
    except Exception as ex:
        raise Exception(f"Error al crear materia: {str(ex)}")


async def update_materia(materia: dict):
    try:
        m = await Materia.get_or_none(id=materia["id"])
        if not m:
            return 0

        # Update basic materia fields
        m.nombre = materia["nombre"]

        if materia["semestre"] > 1:
            m.prelacion = materia["prelacion"]
        else:
            m.prelacion = ""
        m.unidad_credito = materia["unidad_credito"]
        m.hp = materia["hp"]
        m.ht = materia["ht"]
        m.semestre = materia["semestre"]
        m.id_carrera_id = materia["id_carrera"]
        m.maximo = materia["maximo"]

        await m.save()

        # Handle asignaciones if provided
        if "asignaciones" in materia:
            # Delete existing asignaciones
            await AsignacionMateria.filter(materia_id=materia["id"]).delete()

            # Create new asignaciones
            for asignacion in materia["asignaciones"]:
                horarios = []
                if asignacion.get("horarios"):
                    for horario in asignacion["horarios"]:
                        horarios.append({
                            "dia": horario["dia"],
                            "hora_inicio": horario["hora_inicio"],
                            "hora_fin": horario["hora_fin"]
                        })

                await AsignacionMateria.create(
                    materia=m,
                    profesor_id=asignacion.get("profesor_id") if asignacion.get("profesor_id") else None,
                    horarios=horarios,
                    nombre=asignacion.get("nombre", "")
                )

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
            ).prefetch_related("id_carrera")
        else:
            materias = await Materia.filter(
                id_carrera=estudiante.carrera_id,
                semestre__lte=estudiante.semestre
            ).prefetch_related("id_carrera")

        for materia in materias:
            # Get asignaciones for this materia
            asignaciones = await AsignacionMateria.filter(
                materia_id=materia.id
            ).prefetch_related("profesor__usuario")

            # Skip materias without asignaciones (no professor assigned)
            if not asignaciones:
                continue

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

            count = await Matricula.filter(cod_materia=materia, ciclo=ciclo).count()

            # Process asignaciones data
            asignaciones_data = []
            for asig in asignaciones:
                horarios = asig.horarios or []
                if isinstance(horarios, str):
                    try:
                        horarios = json.loads(horarios)
                    except json.JSONDecodeError:
                        horarios = []

                asignaciones_data.append({
                    "id": asig.id,
                    "nombre": asig.nombre,
                    "horarios": horarios,
                    "profesor": {
                        "id": asig.profesor.id,
                        "nombre": asig.profesor.usuario.nombre,
                    }
                })

            materias_validas.append({
                "id": materia.id,
                "nombre": materia.nombre,
                "prelacion": materia.prelacion,
                "unidad_credito": materia.unidad_credito,
                "hp": materia.hp,
                "ht": materia.ht,
                "semestre": materia.semestre,
                "id_carrera": materia.id_carrera_id,
                "maximo": materia.maximo,
                "cantidad_estudiantes": count,
                "carrera": {
                    "id": materia.id_carrera.id,
                    "nombre": materia.id_carrera.nombre
                },
                "asignaciones": asignaciones_data
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
                "carrera": materia.id_carrera.nombre,
                "activo": materia.activo
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


async def delete_materia(materia_id):
    try:
        materia = await Materia.get(id=materia_id)
        materia.activo = False
        await materia.save()
        return 1
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
        ).prefetch_related("id_carrera")

        resultado = {"contenido": {"materia": []}}

        for m in materias:
            # Get asignaciones for this materia
            asignaciones = await AsignacionMateria.filter(
                materia_id=m.id
            ).prefetch_related("profesor__usuario")

            asignaciones_data = []
            for asig in asignaciones:
                horarios = asig.horarios or []
                if isinstance(horarios, str):
                    try:
                        horarios = json.loads(horarios)
                    except json.JSONDecodeError:
                        horarios = []

                if asig.profesor and asig.profesor.usuario:
                    asignaciones_data.append({
                        "id": asig.id,
                        "nombre": asig.nombre,
                        "horarios": horarios,
                        "profesor": {
                            "cedula": asig.profesor.usuario.cedula,
                            "nombre": asig.profesor.usuario.nombre,
                            "titulo": asig.profesor.titulo
                        }
                    })

            resultado["contenido"]["materia"].append({
                "id": m.id,
                "nombre": m.nombre,
                "prelacion": m.prelacion,
                "unidad_credito": m.unidad_credito,
                "hp": m.hp,
                "ht": m.ht,
                "semestre": m.semestre,
                "id_carrera": m.id_carrera_id,
                "maximo": m.maximo,
                "carrera": m.id_carrera.nombre if m.id_carrera else None,
                "asignaciones": asignaciones_data
            })

        return resultado

    except Exception as ex:
        raise Exception(ex)


async def get_materia_con_nombre_y_config(materia_id: str):
    try:
        materia = await Materia.get_or_none(id=materia_id).prefetch_related("id_carrera")
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
