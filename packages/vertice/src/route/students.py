from flask import Blueprint, jsonify, request
from packages.vertice.src.service.configuracion import ConfigModel
from service.entities.students import Student
from service.entities.pagos import Pago
from packages.vertice.src.service.estudiantes import StudentModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta, datetime
import traceback
from packages.vertice.src.service.trazabilidad import TrazabilidadModel
from service.entities.trazabilidad import Trazabilidad

main = Blueprint('students_blueprint', __name__)

@main.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@main.route('/')
@jwt_required()
def get_students():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        students = StudentModel.get_students()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener todos los estudiantes",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="General",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": students})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}), 500

@main.route('/<cedula>')
@jwt_required()
def get_student(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        student = StudentModel.get_student(cedula)
        
        if student is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener estudiante con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="General",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": student})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@main.route('/add', methods=["POST"])
@jwt_required()
def add_student():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        estado = request.json['estado']
        carrera = request.json['carrera']
        password = generate_password_hash(request.json["password"], method="sha256")
        edad = request.json['edad']
        sexo = request.json['sexo']
        direccion = request.json['direccion']
        fecha_nac = datetime.strptime(request.json['fecha_nac'], "%d-%m-%Y")

        student = Student(str(cedula), fullname, correo, telefono, semestre, password, estado, carrera, edad, sexo, 0, direccion, fecha_nac)
        affected_rows = StudentModel.add_student(student)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir estudiante con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Administración",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@main.route('/update/<cedula>', methods=["PUT"])
@jwt_required()
def update_student(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        estado = request.json['estado']
        carrera = request.json["carrera"]
        edad = request.json['edad']
        sexo = request.json['sexo']
        direccion = request.json['direccion']
        fecha_nac = datetime.strptime(request.json['fecha_nac'], "%d-%m-%Y")

        student = Student(str(cedula), fullname, correo, telefono, semestre, None, estado, carrera, edad, sexo, 0, direccion, fecha_nac)
        affected_rows = StudentModel.update_student(student)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar estudiante con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Administración",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@main.route('/delete/<cedula>', methods=["DELETE"])
@jwt_required()
def delete_student(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        student = Student(str(cedula))
        affected_rows = StudentModel.delete_student(student)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar estudiante con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Estudiantes",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@main.route("/add-materia/<materia>", methods=["POST"])
@jwt_required()
def add_student_to_materia(materia: str):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        correo_estudiante = claims.get('sub')
        student: Student | None
        if correo_estudiante is not None:
            print(correo_estudiante)
            student_entity = Student(correo=correo_estudiante)
            student = StudentModel.login(student_entity)
            if student is not None:
                affected_rows = StudentModel.add_materia(student, materia)
                if affected_rows == 1:
                    print(student)
                    # Registrar trazabilidad
                    trazabilidad = Trazabilidad(
                        accion=f"Añadir materia {materia} al estudiante con cédula: {student.cedula}",
                        usuario=usuario,
                        fecha=datetime.now(),
                        modulo="Estudiantes",
                        nivel_alerta=2
                    )
                    TrazabilidadModel.add_trazabilidad(trazabilidad)

                    return jsonify({"ok": True, "status": 200, "data": None}), 200
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}})

@main.route("/materias", methods=["GET"])
@jwt_required()
def get_notas():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        correo_estudiante = claims.get('sub')
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)
            student_entity = StudentModel.login(student_entity)
            notas_obj = StudentModel.get_notas_estudiante(student_entity.cedula)
            
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener notas del estudiante con cédula: {student_entity.cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="General",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": notas_obj}), 200
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@main.route("/historico", methods=["GET"])
@jwt_required()
def get_historico():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        correo_estudiante = claims.get('sub')
        student: Student | None
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)
            student_entity = StudentModel.login(student_entity)
            notas_obj = StudentModel.get_historico(student_entity.cedula)
            
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener histórico del estudiante con cédula: {student_entity.cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Estudiantes",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": notas_obj}), 200
    except Exception as ex:
        print(ex.with_traceback(None))
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@main.route("/horario", methods=["GET"])
@jwt_required()
def get_horario():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        correo_estudiante = claims.get('sub')
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)
            student_entity = StudentModel.login(student_entity)
            materias = StudentModel.get_inscritas(student_entity.cedula)
            
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener horario del estudiante con cédula: {student_entity.cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Estudiantes",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": {"materias": materias}}), 200
    except Exception as ex:
        print(ex.with_traceback(None))
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@main.route('/login', methods=["POST"])
def login_estudiante():
    try:
        fecha_actual = datetime.now()
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        estudiante = Student(correo=usuario)
        estudiante = StudentModel.login(estudiante)
        if estudiante is not None:
            if estudiante.estado == "abandonó":
                return jsonify({"ok": False, "status": 401, "data": {"message": "Por favor, dirígete a tu centro de estudios"}}), 401
            elif check_password_hash(estudiante.password, clave):
                # Validar pagos
                pagos: list[Pago] = StudentModel.get_pago_by_student(estudiante.cedula)
                config = ConfigModel.get_configuracion("1")

                for concepto in ["pre_inscripcion", "inscripcion"]:
                    pago_realizado = any(pago.monto_id.concepto == concepto and pago.ciclo == config.ciclo for pago in pagos)
                    if not pago_realizado:
                        return jsonify({"ok": False, "status": 401, "data": {"message": f"No has realizado el pago de la {concepto.replace('_', ' ').capitalize()}"}}), 401

                for i in range(1, 6):
                    fecha_cuota = getattr(config, f'cuota{i}').strftime("%Y-%m-%d")
                    if fecha_actual >= datetime.strptime(fecha_cuota, "%Y-%m-%d"):
                        pago_realizado = any(pago.monto_id.concepto == f'cuota{i}' and pago.ciclo == config.ciclo for pago in pagos)
                        if not pago_realizado:
                            return jsonify({"ok": False, "status": 401, "data": {"message": f"No has realizado el pago de la cuota {i}"}}), 401

                access_token = create_access_token(identity=estudiante.correo, expires_delta=timedelta(hours=2), additional_claims={'rol': 'E', 'nombre': estudiante.fullname})

                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Inicio de sesión del estudiante con cédula: {estudiante.cedula}",
                    usuario=estudiante.fullname,
                    fecha=datetime.now(),
                    modulo="Autenticacion",
                    nivel_alerta=1
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": {"estudiante": estudiante.to_JSON(), "access_token": f"Bearer {access_token}"}})
            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route('/refresh')
@jwt_required()
def jwt_student():
    try:
        correo_estudiante = get_jwt_identity()  # Esto obtiene la identidad del token, en este caso, un correo
        student: Student | None
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)
            student = StudentModel.login(student_entity)
            if student is not None:
                # Registrar trazabilidad

                return jsonify({"ok": True, "status": 200, "data": student.to_JSON()})
            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "no autorizado"}}), 401
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

