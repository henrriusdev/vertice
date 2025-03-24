from service.entities.coordinacion import Coordinacion
from service.coordinacionmodel import CoordinacionModel
from service.studentsmodel import StudentModel, Student
from packages.vertice.src.service.trazabilidad import TrazabilidadModel
from service.entities.trazabilidad import Trazabilidad
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from logging import Logger

logger = Logger(__name__, 1)


coordinacion = Blueprint('coordinacion_blueprint', __name__)

@coordinacion.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@coordinacion.route('/')
@jwt_required()
def get_coordinadores():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        coordinadores = CoordinacionModel.get_coordinadores()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener Coordinadores",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Coordinacion",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status":200, "data": coordinadores})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@coordinacion.route('/<cedula>')
@jwt_required()
def get_coordinador(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        coordinador = CoordinacionModel.get_coordinador(cedula)
        
        if coordinador != None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener Coordinador con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Coordinacion",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status":200, "data": coordinador})
        else:
            return jsonify({"ok": False, "status":404, "data":{"message": "coordinador no encontrado"}}), 404
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}), 500

@coordinacion.route('/add', methods=["POST"])
@jwt_required()
def add_coordinador():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        coordinador = Coordinacion(str(cedula), fullname, correo, telefono, password)
        affected_rows = CoordinacionModel.add_coordinador(coordinador)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir Coordinador con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Coordinacion",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@coordinacion.route('/update/<cedula>', methods=["PUT"])
@jwt_required()
def update_coordinador(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        coordinador = Coordinacion(str(cedula), fullname, correo, telefono, password)
        affected_rows = CoordinacionModel.update_coordinador(coordinador)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar Coordinador con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Coordinacion",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@coordinacion.route('/delete/<cedula>', methods=["DELETE"])
@jwt_required()
def delete_coordinador(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        coordinador = Coordinacion(str(cedula))
        affected_rows = CoordinacionModel.delete_coordinador(coordinador)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar Coordinador con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Coordinacion",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "coordinador no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@coordinacion.route("/materias/<cedula>", methods=["GET"])
@jwt_required()
def get_nota(cedula: str):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        notas_obj = StudentModel.get_notas_estudiante(cedula)
        
        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion=f"Obtener Notas del Estudiante con cédula: {cedula}",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Estudiante",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": notas_obj}), 200
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@coordinacion.route('/login', methods=["POST"])
def login_coordinacion():
    try:
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        coordinador = Coordinacion(correo=usuario)
        coordinador = CoordinacionModel.login(coordinador)
        if coordinador is not None:
            if check_password_hash(coordinador.password, clave):
                access_token = create_access_token(identity=coordinador.correo, expires_delta=timedelta(hours=2), additional_claims={'rol': 'CO', 'nombre': coordinador.fullname})
                
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Inicio de sesión del coordinador con cédula: {coordinador.cedula}",
                    usuario=coordinador.correo,
                    fecha=datetime.now(),
                    modulo="Autenticacion",
                    nivel_alerta=1
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": {"coordinador": coordinador.to_JSON(), "access_token": f"Bearer {access_token}"}})
            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@coordinacion.route('/refresh')
@jwt_required()
def jwt_coordinador():
    try:
        correo_coordinador = get_jwt_identity()  # Esto obtiene la identidad del token, en este caso, un correo
        coordinador: Coordinacion | None  # Declaramos sin iniciar la variable del coordinador
        if correo_coordinador is not None:
            coordinador_entity = Coordinacion(correo=correo_coordinador)  # Creamos la entidad del coordinador
            coordinador = CoordinacionModel.login(coordinador_entity)  # Revisamos la bd
            if coordinador != None:
                return jsonify({"ok": True, "status": 200, "data": coordinador.to_JSON()})  # Retornamos si es correcto
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "no autorizado"}}), 401
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@coordinacion.route('/promedio-ponderado/<cedula_estudiante>', methods=['GET'])
@jwt_required()
def obtener_promedio_ponderado(cedula_estudiante):
    try:
        # Verificar si el usuario autenticado es un coordinador o el propio estudiante
        correo_autenticado = get_jwt_identity()
        if correo_autenticado != cedula_estudiante:
            return jsonify({"ok": False, "status": 401, "data": {"message": "No autorizado"}}), 401

        # Calcular el promedio ponderado del estudiante
        promedio_ponderado = CoordinacionModel.calcular_promedio_ponderado_estudiante(cedula_estudiante)

        if promedio_ponderado is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener Promedio Ponderado del Estudiante con cédula: {cedula_estudiante}",
                usuario=correo_autenticado,
                fecha=datetime.now(),
                modulo="Estudiante",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": {"promedio_ponderado": promedio_ponderado}}), 200
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "No se encontraron notas para este estudiante"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@coordinacion.route('/update-password', methods=["PATCH"])
@jwt_required()
def update_password_coordinador():
    try:
        claims = get_jwt()
        usuario = claims.get('sub')
        nombre = claims.get('nombre')

        current_password = request.json['current_password']
        new_password = request.json['new_password']
        logger.info(current_password, new_password)

        coordinador = CoordinacionModel.get_coordinador_by_correo(usuario)
    
        if coordinador and check_password_hash(coordinador.password, current_password):
            new_password = generate_password_hash(new_password, method="sha256")
            affected_rows = CoordinacionModel.update_password(usuario, new_password)
            if affected_rows == 1:
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Actualizar contraseña del coordinador: {nombre}",
                    usuario=usuario,
                    fecha=datetime.now(),
                    modulo="Coordinación",
                    nivel_alerta=2
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})
            else:
                return jsonify({"ok": False, "status": 500, "data": "Error al actualizar la contraseña"}), 500
        else:
            logger.info(coordinador.password, current_password, check_password_hash(coordinador.password, current_password))
            
            return jsonify({"ok": False, "status": 401, "data": "Contraseña actual incorrecta"}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500