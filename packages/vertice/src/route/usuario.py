import traceback
from datetime import timedelta, datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from src.middleware.sesion import unica_sesion_requerida
from src.model.usuario import Usuario
from src.service.sesiones import eliminar_sesion_por_jti, registrar_sesion
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import bloquear_usuario, delete_usuario, get_usuarios, login, reactivar_usuario, \
    update_password, get_usuario_por_correo, registrar_usuario, update_usuario

usr = Blueprint('usuario_blueprint', __name__)


@usr.post('/login')
async def login_usuario():
    try:
        data = request.json
        correo = data.get('correo')
        password = data.get('password')

        usuario = await login(correo, password)
        print(not usuario)
        if not usuario:
            return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401

        claims = {
            'sub': usuario.correo,
            'rol': usuario.rol.nombre[0].upper(),
            'nombre': usuario.nombre
        }

        access_token = create_access_token(
            identity=usuario.correo,
            expires_delta=timedelta(hours=2),
            additional_claims=claims
        )

        # Extraer jti del token generado
        jti = decode_token(access_token)["jti"]

        await registrar_sesion(usuario.correo, jti)

        await add_trazabilidad({
            "accion": f"Inicio de sesión del usuario: {usuario.correo}",
            "usuario": usuario,
            "fecha": datetime.now(),
            "modulo": "Autenticación",
            "nivel_alerta": 1
        })

        return jsonify({
            "ok": True,
            "status": 200,
            "data": {
                "usuario": usuario.to_dict(),
                "access_token": f"Bearer {access_token}"
            }
        })

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.post('/logout')
@jwt_required()
@unica_sesion_requerida
async def logout_usuario():
    try:
        jti = get_jwt().get("jti")

        eliminado = await eliminar_sesion_por_jti(jti)
        if not eliminado:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Sesión no encontrada"}}), 404

        return jsonify({"ok": True, "status": 200, "data": "Sesión cerrada correctamente"})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.get('/refresh')
@jwt_required()
@unica_sesion_requerida
async def refresh_usuario():
    try:
        correo = get_jwt_identity()
        usuario = await get_usuario_por_correo(correo)
        await usuario.fetch_related('rol')
        if not usuario:
            return jsonify({"ok": False, "status": 401, "data": {"message": "No autorizado"}}), 401

        return jsonify({"ok": True, "status": 200, "data": usuario.to_dict()})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.patch('/update-password')
@jwt_required()
@unica_sesion_requerida
async def update_usuario_password():
    try:
        claims = get_jwt()
        correo = claims.get('sub')
        nombre = claims.get('nombre')
        data = request.json

        current_password = data['current_password']
        new_password = data['new_password']

        usuario = await get_usuario_por_correo(correo)
        if not usuario or not check_password_hash(usuario.password, current_password):
            return jsonify({"ok": False, "status": 401, "data": {"message": "Contraseña actual incorrecta"}}), 401

        hashed = generate_password_hash(new_password, method="pbkdf2:sha256", salt_length=16)
        await update_password(correo, hashed)

        await add_trazabilidad({
            'accion': f"Actualizar contraseña del usuario: {nombre}",
            'usuario': correo,
            'fecha': datetime.now(),
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})

    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.get('/')
@jwt_required()
@unica_sesion_requerida
async def obtener_usuarios():
    try:
        usuarios = await get_usuarios()
        return jsonify({"ok": True, "status": 200, "data": usuarios})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.post('/register')
async def registrar():
    try:
        data = request.json
        # Quitar el prefijo V- o E- de la cédula para usarla como password
        if not data.get('cedula') or not data.get('nombre') or not data.get('correo') or not data.get('rol_id'):
            return jsonify({"ok": False, "status": 400, "data": {"message": "Faltan campos requeridos"}}), 400

        cedula = data['cedula'].replace('V-', '').replace('E-', '')
        usuario = Usuario(
            cedula=data['cedula'],
            nombre=data['nombre'],
            correo=data['correo'],
            password=generate_password_hash(cedula, method="pbkdf2:sha256", salt_length=16),
            rol_id=data['rol_id']
        )

        creado = await registrar_usuario(usuario)

        await add_trazabilidad({
            "accion": f"Registrar usuario: {usuario.correo}, nombre: {usuario.nombre}",
            "usuario": usuario,
            "fecha": datetime.now(),
            "modulo": "Usuarios",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200, "data": creado.to_dict()})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.put('/update/<int:id>')
@jwt_required()
@unica_sesion_requerida
async def update(id):
    try:
        payload = request.json
        await update_usuario(id, payload)
        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.patch("/bloquear/<correo>")
@jwt_required()
@unica_sesion_requerida
async def bloquear(correo):
    try:
        claims = get_jwt()
        admin = claims.get("nombre")

        success = await bloquear_usuario(correo)
        if not success:
            return jsonify(
                {"ok": False, "status": 404, "data": {"message": "Usuario no encontrado o ya estaba inactivo"}}), 404

        return jsonify({"ok": True, "status": 200, "data": f"Usuario {correo} bloqueado correctamente"})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.patch("/reactivar/<correo>")
@jwt_required()
@unica_sesion_requerida
async def reactivar(correo):
    try:
        claims = get_jwt()
        admin = claims.get("nombre")

        success = await reactivar_usuario(correo)
        if not success:
            return jsonify(
                {"ok": False, "status": 404, "data": {"message": "Usuario no encontrado o ya estaba activo"}}), 404

        return jsonify({"ok": True, "status": 200, "data": f"Usuario {correo} reactivado correctamente"})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.delete('/delete/<cedula>')
@jwt_required()
@unica_sesion_requerida
async def delete(cedula):
    try:
        await delete_usuario(cedula)
        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.patch('/force-password')
@jwt_required()
@unica_sesion_requerida
async def force_password():
    try:
        claims = get_jwt()
        correo = claims.get('sub')
        
        data = request.json
        new_password = data.get('new_password')

        if not new_password:
            return jsonify({"ok": False, "status": 400, "data": {"message": "Nueva contraseña es requerida"}}), 400

        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        # Actualizar la contraseña
        usuario.password = generate_password_hash(new_password, method="pbkdf2:sha256", salt_length=16)
        usuario.cambiar_clave = False
        await usuario.save()

        await add_trazabilidad({
            'accion': f"Actualización forzada de contraseña del usuario: {usuario.nombre}",
            'usuario': usuario,
            'fecha': datetime.now(),
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
