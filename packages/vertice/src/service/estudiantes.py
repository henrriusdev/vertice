from datetime import datetime

from src.utils.fecha import format_fecha, parse_fecha
from src.model.usuario import Usuario
from src.model.estudiante import Estudiante
from src.model.matricula import Matricula
from src.model.configuracion import Configuracion
from src.model.pago import Pago
from tortoise.exceptions import DoesNotExist

async def get_students():
    try:
        estudiantes = await Estudiante.all().prefetch_related("usuario", "carrera").order_by("usuario__cedula")
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
            "fullname": estudiante.usuario.fullname,
            "correo": estudiante.usuario.correo,
            "telefono": estudiante.usuario.telefono,
            "semestre": estudiante.semestre,
            "estado": estudiante.usuario.rol.nombre,
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
        await estudiante.delete()
        await estudiante.usuario.delete()
        return 1
    except Exception as ex:
        raise Exception(ex)


async def add_materia(cedula: str, id_materia: str):
    try:
        estudiante = await Estudiante.get(usuario__cedula=cedula)
        ciclo = (await Configuracion.get(id=1)).ciclo

        await Matricula.create(
            cod_materia_id=id_materia,
            cedula_estudiante=estudiante,
            notas=[0, 0, 0],
            uc=0,
            ciclo=ciclo
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
        estudiante = await Estudiante.get(usuario__cedula=cedula_estudiante)
        matriculas = await Matricula.filter(cedula_estudiante=estudiante).prefetch_related("cod_materia")

        historico = []
        for m in matriculas:
            historico.append({
                "materia": m.cod_materia.nombre,
                "id": m.cod_materia.id,
                "ciclo": m.ciclo,
                "semestre": m.cod_materia.semestre,
                "notas": m.notas or [],
                "promedio": round(sum(m.notas) / len(m.notas), 2) if m.notas else 0
            })

        return {
            "notas": historico
        }

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
                "modalidad": m.cod_materia.modalidad,
                "asignatura": f"{m.cod_materia.id} {m.cod_materia.nombre}"
            })

        return join

    except Exception as ex:
        raise Exception(ex)


async def get_inscritas(cedula: str):
    try:
        ciclo = (await Configuracion.get(id=1)).ciclo
        estudiante = await Estudiante.get(usuario__cedula=cedula)

        matriculas = await Matricula.filter(
            cedula_estudiante=estudiante,
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
                "dia": ", ".join([h["dia"] for h in horarios]),
                "hora_inicio": ", ".join([h["hora_inicio"] for h in horarios]),
                "hora_fin": ", ".join([h["hora_fin"] for h in horarios]),
                "unidad_credito": materia.unidad_credito,
                "id_docente": docente.fullname if docente else None
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
        pagos = await Pago.filter(cedula_estudiante=estudiante).prefetch_related("monto_id")
        config = await Configuracion.get(id=1)
        ciclo = config.ciclo
        fecha_actual = datetime.now().date()

        # Verificar pre_inscripcion e inscripcion
        for concepto in ["pre_inscripcion", "inscripcion"]:
            pagado = any(
                p.monto_id.concepto == concepto and p.ciclo == ciclo
                for p in pagos
            )
            if not pagado:
                raise Exception(f"No has realizado el pago de la {concepto.replace('_', ' ')}")

        # Verificar cuotas según configuración
        cuotas = config.cuotas or []
        for i, fecha in enumerate(cuotas):
            if fecha_actual >= fecha.date():
                concepto_cuota = f"cuota{i+1}"
                pagado = any(
                    p.monto_id.concepto == concepto_cuota and p.ciclo == ciclo
                    for p in pagos
                )
                if not pagado:
                    raise Exception(f"No has realizado el pago de la {concepto_cuota}")

    except DoesNotExist:
        raise Exception("El estudiante no está registrado")
    except Exception as ex:
        raise ex
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM estudiantes WHERE correo=%s", (correo,))
                row = cursor.fetchone()
                if row:
                    student = Student(
                        cedula=row[0],
                        fullname=row[1],
                        correo=row[2],
                        telefono=row[3],
                        semestre=row[4],
                        password=row[5],
                        estado=row[6],
                        carrera=row[7],
                        edad=row[8],
                        sexo=row[9],
                        direccion=row[10],
                        fecha_nac=row[11]
                    )
                    return student
                else:
                    return None
            connection.close()
        except Exception as ex:
            raise Exception(ex)