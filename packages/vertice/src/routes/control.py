from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token
from datetime import timedelta, datetime
from services.entities.control import Control
from services.controlmodel import ControlModel
from services.trazabilidadmodel import TrazabilidadModel
from services.entities.trazabilidad import Trazabilidad

control = Blueprint('control_es_blueprint', __name__)

@control.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@control.route('/')
@jwt_required()
def get_todo_control():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        control_es = ControlModel.get_todo_control()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener todo el Control",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Control de estudios",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": control_es})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@control.route('/<cedula>')
@jwt_required()
def get_control(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        control_es = ControlModel.get_control(cedula)
        
        if control_es is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener Control con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Control de estudios",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": control_es})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "usuario no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@control.route('/add', methods=["POST"])
@jwt_required()
def add_control():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        control_es = Control(str(cedula), fullname, correo, telefono, password)
        affected_rows = ControlModel.add_control(control_es)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir Control con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Control de estudios",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@control.route('/update/<cedula>', methods=["PUT"])
@jwt_required()
def update_coordinador(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        control_es = Control(str(cedula), fullname, correo, telefono, password)
        affected_rows = ControlModel.update_control(control_es)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar Control con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Control de estudios",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@control.route('/delete/<cedula>', methods=["DELETE"])
@jwt_required()
def delete_coordinador(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        control_es = Control(str(cedula))
        affected_rows = ControlModel.delete_control(control_es)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar Control con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Control de estudios",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "usuario no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@control.route('/login', methods=["POST"])
def login_control():
    try:
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        control_estudio = Control(correo=usuario)
        control_estudio = ControlModel.login(control_estudio)
        if control_estudio is not None:
            # if check_password_hash(ontrol_estudio.password, clave):
                access_token = create_access_token(identity=control_estudio.correo, expires_delta=timedelta(hours=2), additional_claims={'rol': 'CE', 'nombre': control_estudio.fullname})
                
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Inicio de sesión del control con cédula: {control_estudio.cedula}",
                    usuario=control_estudio.correo,
                    fecha=datetime.now(),
                    modulo="Autenticacion",
                    nivel_alerta=1
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": {"control_estudio": control_estudio.to_JSON(), "access_token": f"Bearer {access_token}"}})
            # else:
            #     return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@control.route('/refresh')
@jwt_required()
def jwt_coordinador():
    try:
        correo_coordinador = get_jwt_identity()  # Esto obtiene la identidad del token, en este caso, un correo
        control_estudio: Control | None  # Declaramos sin iniciar la variable del control_estudio
        if correo_coordinador is not None:
            coordinador_entity = Control(correo=correo_coordinador)  # Creamos la entidad del control_estudio
            control_estudio = ControlModel.login(coordinador_entity)  # Revisamos la bd
            if control_estudio != None:
                return jsonify({"ok": True, "status": 200, "data": control_estudio.to_JSON()})  # Retornamos si es correcto
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "no autorizado"}}), 401
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@control.route('/update-password', methods=["PATCH"])
@jwt_required()
def update_password_control():
    try:
        claims = get_jwt()
        usuario = claims.get('sub')
        nombre = claims.get('nombre')

        current_password = request.json['current_password']
        new_password = request.json['new_password']

        control_user = ControlModel.get_control_by_correo(usuario)
        # if control_user and check_password_hash(control_user.password, current_password):
        if control_user:
            hashed_password = generate_password_hash(new_password, method="sha256")
            affected_rows = ControlModel.update_password(usuario, hashed_password)
            if affected_rows == 1:
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Actualizar contraseña del usuario de control: {nombre}",
                    usuario=nombre,
                    fecha=datetime.now(),
                    modulo="Control de estudios",
                    nivel_alerta=2
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})
            else:
                return jsonify({"ok": False, "status": 500, "data": "Error al actualizar la contraseña"}), 500
        else:
            return jsonify({"ok": False, "status": 401, "data": "Contraseña actual incorrecta"}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
