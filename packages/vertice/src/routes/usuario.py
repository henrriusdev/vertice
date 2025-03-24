from datetime import timedelta, datetime
import traceback
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from services.entities.user import User
from services.usermodel import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from services.trazabilidadmodel import TrazabilidadModel
from services.entities.trazabilidad import Trazabilidad

user = Blueprint('user_blueprint', __name__)

@user.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@user.route('/register', methods=["POST"])
def register():
    try:
        usuario = request.json['usuario']
        nombre = request.json['nombre']
        clave = generate_password_hash(request.json["clave"], method="sha256")

        user = User(id=None, usuario=usuario, clave=clave, nombre=nombre)
        affected_rows = UserModel.register(user)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Registrar usuario: {usuario}, nombre: {nombre}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Usuarios",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"register": True})
        else:
            return jsonify({"register": False}), 500
    except Exception as ex:
        return jsonify({"register": str(ex)}), 500

@user.route('/login', methods=["POST"])
def login():
    try:
        usuario = request.json['usuario']
        clave = request.json['clave']
        user = User(usuario, clave)
        user = UserModel.get_user(user)

        if user:
            if check_password_hash(user.clave, clave):
                access_token = create_access_token(identity=user.usuario, expires_delta=timedelta(hours=2), additional_claims={'rol': 'S',  "nombre": user.nombre})
                
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Inicio de sesión del usuario: {usuario}",
                    usuario=usuario,
                    fecha=datetime.now(),
                    modulo="Autenticacion",
                    nivel_alerta=1
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": {"usuario": user.to_JSON(), "access_token": f"Bearer {access_token}"}})
            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": 'Correo y/o contraseña inválidoss'}}), 401
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": 'Correo y/o contraseña inválidosss'}}), 401
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": 'Correo y/o contraseña inválidos'}}), 401

@user.route('/refresh')
@jwt_required()
def jwt_student():
    try:
        usuario = get_jwt_identity()  # esto obtiene la identidad del token, en este caso, un correo
        user: User | None  # declaramos sin iniciar la variable del estudiante
        if usuario is not None:
            usuario_entity = User(usuario=usuario)  # creamos la entidad del estudiante
            user = UserModel.login(usuario_entity)  # revisamos la bd
            if user is not None:
                # Registrar trazabilidad

                return jsonify({"ok": True, "status": 200, "data": user.to_JSON()})
            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "no autorizado"}}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 401, "data": {"message": str(ex)}}), 401

@user.route('/update/clave', methods=["PUT"])
@jwt_required()
def update_clave():
    try:
        claims = get_jwt()
        rol = claims.get('rol')
        usuario = claims.get('nombre')
        if rol != 'S':
            return jsonify({"message": "No autorizado"}), 403

        nuevo = request.json['nuevo']
        nuevo = generate_password_hash(nuevo, "sha256")
        
        user = User("caja_pascal", nuevo)
        affected_rows = UserModel.update_user(user)
        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar clave del usuario: {usuario}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Usuarios",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"successful": True})
        else:
            return jsonify({"successful": False})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
