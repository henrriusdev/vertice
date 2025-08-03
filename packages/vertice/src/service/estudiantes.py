from datetime import datetime

from src.utils.fecha import format_fecha, parse_fecha, now_in_venezuela
from src.model.usuario import Usuario
from src.model.estudiante import Estudiante
from src.model.matricula import Matricula
from src.model.configuracion import Configuracion
from src.model.pago import Pago
from tortoise.exceptions import DoesNotExist

async def get_students(carrera_id=None):
    try:
        if carrera_id is not None:
            estudiantes = await Estudiante.filter(carrera_id=carrera_id).prefetch_related("usuario", "carrera").order_by("usuario__nombre")
        else:
            estudiantes = await Estudiante.all().prefetch_related("usuario", "carrera").order_by("usuario__nombre")
        return [
            {
                "cedula": e.usuario.cedula,
                "nombre": e.usuario.nombre,
                "correo": e.usuario.correo,
                "semestre": e.semestre,
                "carrera": e.carrera.nombre,
                "edad": e.edad,
                "sexo": e.sexo,
                "promedio": float(e.promedio),
                "direccion": e.direccion,
                "fecha_nacimiento": e.fecha_nac.isoformat(),
                "id": e.id,
                "activo": e.usuario.activo,
                "usuario": {
                    "id": e.usuario.id
                }
            }
            for e in estudiantes
        ]
    except Exception as ex:
        raise Exception(ex)


async def get_student(cedula: str):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula).prefetch_related("usuario", "carrera")
        return {
            "cedula": estudiante.usuario.cedula,
            "nombre": estudiante.usuario.nombre,
            "correo": estudiante.usuario.correo,
            "semestre": estudiante.semestre,
            "activo": estudiante.usuario.activo,
            "carrera": estudiante.carrera.nombre,
            "edad": estudiante.edad,
            "sexo": estudiante.sexo,
            "promedio": float(estudiante.promedio),
            "direccion": estudiante.direccion,
            "fecha_nacimiento": format_fecha(estudiante.fecha_nac)
        }
    except Exception as ex:
        raise Exception(ex)


async def add_student(data):
    try:
        usuario = await Usuario.filter(id=data["usuario"]).first()
        await Estudiante.create(
            usuario=usuario,
            semestre=data["semestre"],
            carrera_id=data["carrera"],
            promedio=data["promedio"],
            direccion=data["direccion"],
            fecha_nac=parse_fecha(data["fecha_nac"]),
            edad=data["edad"],
            sexo=data["sexo"]
        )
        return usuario
    except Exception as ex:
        raise Exception(ex)



async def update_student(id_estudiante: int, data: dict):
    try:
        estudiante = await Estudiante.get(id=id_estudiante).prefetch_related("usuario")

        # Actualizar datos académicos (estudiante)
        estudiante.semestre = data["semestre"]
        estudiante.carrera_id = data["carrera"]
        estudiante.promedio = data["promedio"]
        estudiante.edad = data["edad"]
        estudiante.sexo = data["sexo"]
        estudiante.direccion = data["direccion"]
        estudiante.fecha_nac = parse_fecha(data["fecha_nac"])
        await estudiante.save()

        return 1
    except Exception as ex:
        raise Exception(ex)


async def delete_student(cedula: str):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula)
        usuario = await estudiante.usuario
        usuario.activo = False
        await usuario.save()
        return 1
    except Exception as ex:
        raise Exception(ex)


async def toggle_student_status(cedula: str):
    """
    Toggle the active status of a student (activate/deactivate)
    """
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula)
        usuario = await estudiante.usuario
        # Toggle the active status
        usuario.activo = not usuario.activo
        await usuario.save()
        return usuario.activo  # Return the new status
    except DoesNotExist:
        return False
    except Exception as ex:
        raise Exception(ex)


async def add_materia(cedula: str, id_materias: list[str]):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula)
        config = (await Configuracion.get(id=1))
        notas = [0 for _ in range(config.num_porcentaje)]
        for id_materia in id_materias:
            await Matricula.create(
                cod_materia_id=id_materia,
                cedula_estudiante=estudiante,
                notas=notas,
                uc=0,
                ciclo=config.ciclo
            )
        return 1
    except Exception as ex:
        raise Exception(ex)


async def get_notas_estudiante(cedula_estudiante: str):
    try:
        ciclo = (await Configuracion.get(id=1)).ciclo
        estudiante = await Estudiante.get(usuario__cedula=cedula_estudiante)
        
        matriculas = await Matricula.filter(
            cedula_estudiante=estudiante, ciclo=ciclo
        ).prefetch_related("cod_materia")

        notas = []
        for m in matriculas:
            notas.append({
                "materia": m.cod_materia.nombre,
                "id": m.cod_materia.id,
                "notas": m.notas or [],
                "promedio": round(sum(m.notas) / len(m.notas), 2) if m.notas else 0
            })

        return {
            "notas": notas,
            "ciclo": ciclo
        }

    except Exception as ex:
        raise Exception(ex)


async def get_historico(cedula_estudiante: str):
    try:
        print(cedula_estudiante)
        matriculas = await Matricula.filter(cedula_estudiante__usuario__cedula=cedula_estudiante).prefetch_related("cod_materia", "cod_materia__id_docente__usuario")
        print(len(matriculas))

        historico = []
        for m in matriculas:
            historico.append({
                "nombre": m.cod_materia.nombre,
                "id": m.cod_materia.id,
                "ciclo": m.ciclo,
                "unidad_credito": m.uc,
                "semestre": m.cod_materia.semestre,
                "notas": m.notas or [],
                "prelacion": m.cod_materia.prelacion,
                "promedio": round(sum(m.notas) / len(m.notas), 2) if m.notas else 0,
                "docente": m.cod_materia.id_docente.usuario.nombre
            })

        return historico

    except Exception as ex:
        raise Exception(ex)


async def get_materias_inscritas(cedula: str):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula)
        matriculas = await Matricula.filter(cedula_estudiante=estudiante).prefetch_related("cod_materia")

        join = {"ciclo": "", "contenido": []}

        for m in matriculas:
            join["ciclo"] = m.ciclo  # El último ciclo queda guardado, puedes normalizar si necesitas múltiples
            join["contenido"].append({
                "asignatura": f"{m.cod_materia.id} {m.cod_materia.nombre}"
            })

        return join

    except Exception as ex:
        raise Exception(ex)


async def get_inscritas(cedula: str):
    try:
        ciclo = (await Configuracion.get(id=1)).ciclo

        matriculas = await Matricula.filter(
            cedula_estudiante__usuario__cedula=cedula,
            ciclo=ciclo
        ).prefetch_related("cod_materia__id_docente__usuario")

        resultado = []

        for m in matriculas:
            materia = m.cod_materia
            docente = materia.id_docente.usuario if materia.id_docente else None
            horarios = materia.horarios or []

            resultado.append({
                "id": materia.id,
                "nombre": materia.nombre,
                "hp": materia.hp,
                "ht": materia.ht,
                "horarios": horarios,
                "unidad_credito": materia.unidad_credito,
                "docente": docente.nombre if docente else None
            })

        return resultado

    except Exception as ex:
        raise Exception(ex)


async def get_pago_by_student(cedula: str):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula)

        pagos = await Pago.filter(cedula_estudiante=estudiante).prefetch_related("metodo_pago_id", "monto_id")

        resultado = []
        for p in pagos:
            resultado.append({
                "id": p.id,
                "cedula_estudiante": estudiante.usuario.cedula,
                "metodo_pago": {
                    "id": p.metodo_pago_id.id,
                    "nombre": p.metodo_pago_id.nombre,
                    "descripcion": p.metodo_pago_id.descripcion
                },
                "monto": {
                    "id": p.monto_id.id,
                    "concepto": p.monto_id.concepto,
                    "monto": p.monto_id.monto
                },
                "fecha_pago": p.fecha_pago.isoformat(),
                "referencia_transferencia": p.referencia_transferencia,
                "ciclo": p.ciclo
            })

        return resultado

    except Exception as ex:
        raise Exception(ex)


async def validar_pagos_estudiante(usuario):
    try:
        estudiante = await Estudiante.get(usuario=usuario)
        
        # Buscar sólo pagos pagados
        pagos = await Pago.filter(
            cedula_estudiante=estudiante,
        )
        
        config = await Configuracion.get(id=1)
        ciclo_actual = config.ciclo
        fecha_actual = now_in_venezuela().date()

        conceptos_requeridos = ["inscripcion","servicios"]
        
        for concepto in conceptos_requeridos:
            if not any(p.concepto == concepto and p.ciclo == ciclo_actual for p in pagos):
                raise Exception(f"No has realizado el pago de la {concepto.replace('_', ' ')}")
        
        # Validar cuotas
        cuotas = config.cuotas or []
        for idx, fecha_cuota in enumerate(cuotas):
            # Parse fecha_cuota if it's a string
            if isinstance(fecha_cuota, str):
                fecha_cuota_dt = parse_fecha(fecha_cuota)
            else:
                fecha_cuota_dt = fecha_cuota
            if fecha_actual >= fecha_cuota_dt.date():
                concepto_cuota = f"cuota{idx + 1}"
                if not any(p.concepto == concepto_cuota and p.ciclo == ciclo_actual for p in pagos):
                    raise Exception(f"No has realizado el pago de la {concepto_cuota}")

    except DoesNotExist:
        raise Exception("El estudiante no está registrado")
    except Exception as e:
        raise e


from src.model.estudiante import Estudiante
from src.model.configuracion import Configuracion
from tortoise.exceptions import DoesNotExist

async def obtener_info_estudiante_para_constancia(cedula: str):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula).prefetch_related("usuario", "carrera")
        config = await Configuracion.get(id=1)

        return {
            "nombre": estudiante.usuario.nombre,
            "cedula": estudiante.usuario.cedula,
            "carrera": estudiante.carrera.nombre,
            "semestre": estudiante.semestre,
            "ciclo": config.ciclo
        }

    except DoesNotExist:
        return None
    except Exception as ex:
        raise Exception(ex)


async def get_active_estudiantes():
    return await Estudiante.filter(usuario__activo=True)
