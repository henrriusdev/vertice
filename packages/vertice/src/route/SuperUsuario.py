from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from service.entities.SuperUsuario import SuperUsuario
from service.SuperUsuarioModel import SuperUsuarioModel
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from packages.vertice.src.service.trazabilidad import TrazabilidadModel
from service.entities.trazabilidad import Trazabilidad
import traceback
superUs = Blueprint('superUsuario_Blueprint', __name__)

@superUs.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@superUs.route('/<cedula>')
@jwt_required()
def get_Super(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        superUs = SuperUsuarioModel.get_super_user(cedula)
        
        if superUs is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener super usuario con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Supervisión",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": superUs})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "super usuario no encontrado"}}), 404
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}), 500

@superUs.route('/add', methods=["POST"])
def add_Super():
    try:
        cedula = request.json['cedula']
        nombre = request.json['nombre']
        correo = request.json['correo']
        password = generate_password_hash(request.json["password"], method="sha256")

        superUs = SuperUsuario(str(cedula), nombre, correo, password)
        affected_rows = SuperUsuarioModel.add_super_user(superUs)

        if affected_rows == 1:
            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@superUs.route('/update/<cedula>', methods=["PUT"])
@jwt_required()
def update_Super(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        nombre = request.json['nombre']
        correo = request.json['correo']
        password = generate_password_hash(request.json["password"], method="sha256")

        superUs = SuperUsuario(str(cedula), nombre, correo, password)
        affected_rows = SuperUsuarioModel.update_super_user(superUs)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar super usuario con cédula: {cedula}, nombre: {nombre}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Supervisión",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@superUs.route('/delete/<cedula>', methods=["DELETE"])
@jwt_required()
def delete_Super(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        superUs = SuperUsuario(str(cedula))
        affected_rows = SuperUsuarioModel.delete_super_user(superUs)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar super usuario con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Supervisión",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "super usuario no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@superUs.route('/login', methods=["POST"])
def login_super_usuario():
    try:
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        super_usuario = SuperUsuario(correo=usuario)
        super_usuario = SuperUsuarioModel.login(super_usuario)
        if super_usuario is not None:
            if check_password_hash(super_usuario.password, clave):
                access_token = create_access_token(identity=super_usuario.correo, expires_delta=timedelta(hours=2), additional_claims={'rol': 'S', 'nombre': super_usuario.nombre})
                
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Inicio de sesión del super usuario con cédula: {super_usuario.cedula}",
                    usuario=super_usuario.correo,
                    fecha=datetime.now(),
                    modulo="Autenticacion",
                    nivel_alerta=1
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": {"Supervisión": super_usuario.to_JSON(), "access_token": f"Bearer {access_token}"}})
            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@superUs.route('/refresh')
@jwt_required()
def jwt_super():
    try:
        correo_super = get_jwt_identity()
        claims = get_jwt()
        rol = claims.get('rol')
        print(rol)
        super_entity: SuperUsuario | None
        
        if correo_super is not None:
            super_entity = SuperUsuario(correo=correo_super)
            super_entity = SuperUsuarioModel.login(super_entity)
            
            if super_entity is not None:

                return jsonify({"ok": True, "status": 200, "data": super_entity.to_JSON()})
            else:
                print(super_entity)
                return jsonify({"ok": False, "status": 401, "data": {"message": "no autorizado"}}), 401
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}), 500


@superUs.route('/update-password', methods=["PATCH"])
@jwt_required()
def update_password_super_usuario():
    try:
        claims = get_jwt()
        usuario = claims.get('sub')
        nombre = claims.get('nombre')

        current_password = request.json['current_password']
        new_password = request.json['new_password']

        super_usuario = SuperUsuarioModel.get_super_usuario_by_correo(usuario)
        if super_usuario and check_password_hash(super_usuario.password, current_password):
            new_password = generate_password_hash(new_password, method="sha256")
            affected_rows = SuperUsuarioModel.update_password(usuario, new_password)
            if affected_rows == 1:
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Actualizar contraseña del super usuario: {nombre}",
                    usuario=nombre,
                    fecha=datetime.now(),
                    modulo="Supervisión",
                    nivel_alerta=2
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})
            else:
                return jsonify({"ok": False, "status": 500, "data": "Error al actualizar la contraseña"}), 500
        else:
            return jsonify({"ok": False, "status": 401, "data": "Contraseña actual incorrecta"}), 401
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500