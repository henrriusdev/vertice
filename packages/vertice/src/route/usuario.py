import traceback
from datetime import timedelta, datetime
from os import getcwd, path, makedirs
import os

from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from src.model.usuario import Usuario
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import bloquear_usuario, delete_usuario, get_usuarios, login, reactivar_usuario, \
    update_password, get_usuario_por_correo, registrar_usuario, update_usuario, toggle_usuario_status
from src.utils.fecha import now_in_venezuela

usr = Blueprint('usuario_blueprint', __name__)

# Configuration for photo uploads
UPLOAD_FOLDER = path.abspath(path.join(getcwd(), "../../uploads/profile_photos/"))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_folder_if_not_exists(folder_path):
    if not path.exists(folder_path):
        makedirs(folder_path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@usr.route('/toggle-status/<cedula>')
@jwt_required()
async def toggle_usuario_status_route(cedula: str):
    try:
        claims = get_jwt()
        usuario = await get_usuario_por_correo(claims.get('sub'))
        
        # Toggle the usuario's status
        result = await toggle_usuario_status(cedula)
        if not result:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        await add_trazabilidad({
            "accion": f"Cambiar estado de usuario {cedula} a {'activo' if result.activo else 'inactivo'}",
            "usuario": usuario,
            "modulo": "Usuarios",
            "nivel_alerta": 2
        })

        return jsonify({
            "ok": True,
            "status": 200,
            "data": {
                "activo": result.activo,
                "message": f"Estado del usuario actualizado exitosamente"
            }
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "ok": False,
            "status": 500,
            "data": {"message": str(e)}
        }), 500

@usr.post('/login')
async def login_usuario():
    try:
        data = request.json
        correo = data.get('correo')
        password = data.get('password')

        result = await login(correo, password)
        
        # Check if result is an error object
        if isinstance(result, dict) and "error" in result:
            error_code = 401  # Default unauthorized
            if result["error"] == "EMAIL_NOT_FOUND":
                error_code = 404  # Not found
            elif result["error"] == "ACCOUNT_INACTIVE":
                error_code = 403  # Forbidden
            
            return jsonify({
                "ok": False, 
                "status": error_code, 
                "data": {
                    "message": result["message"],
                    "error_code": result["error"]
                }
            }), error_code
            
        # If we get here, result is a valid user object
        usuario = result

        claims = {
            'sub': usuario.correo,
            'rol': usuario.rol.nombre,
            'nombre': usuario.nombre
        }

        access_token = create_access_token(
            identity=usuario.correo,
            expires_delta=timedelta(hours=24),
            additional_claims=claims
        )


        await add_trazabilidad({
            "accion": f"Inicio de sesión del usuario: {usuario.correo}",
            "usuario": usuario,
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
async def logout_usuario():
    try:
        return jsonify({"ok": True, "status": 200, "data": "Sesión cerrada correctamente"})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.get('/refresh')
@jwt_required()
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
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})

    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.get('/')
@jwt_required()
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
            "modulo": "Usuarios",
            "nivel_alerta": 2
        })

        return jsonify({"ok": True, "status": 200, "data": creado.to_dict()})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.put('/update/<int:id>')
@jwt_required()
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
async def delete(cedula):
    try:
        await delete_usuario(cedula)
        return jsonify({"ok": True, "status": 200})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.patch('/change-password')
@jwt_required()
async def change_password():
    try:
        claims = get_jwt()
        correo = claims.get('sub')
        datos = request.json

        if not datos.get('current_password') or not datos.get('new_password'):
            return jsonify({"ok": False, "status": 400, "data": {"message": "Contraseña actual y nueva son requeridas"}}), 400

        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        # Validar contraseña actual
        if not usuario.check_password(datos.get("current_password")):
            return jsonify({"ok": False, "status": 401, "data": {"message": "Contraseña actual incorrecta"}}), 401

        # Cambiar contraseña
        usuario.password = generate_password_hash(datos.get("new_password"), method="pbkdf2:sha256", salt_length=16)
        await usuario.save()

        await add_trazabilidad({
            'accion': f"Cambio de contraseña del usuario: {usuario.nombre}",
            'usuario': usuario,
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada correctamente"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@usr.post('/force-password')
async def force_password():
    try:
        datos = request.json
        correo = datos.get('correo')
        password = datos.get('password')

        if not password:
            return jsonify({"ok": False, "status": 400, "data": {"message": "La nueva contraseña es requerida"}}), 400

        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        # Actualizar la contraseña
        usuario.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
        usuario.cambiar_clave = False
        await usuario.save()

        await add_trazabilidad({
            'accion': f"Actualización forzada de contraseña del usuario: {usuario.nombre}",
            'usuario': usuario,
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.post('/first-reset-password')
@jwt_required()
async def first_reset_password():
    try:
        claims = get_jwt()
        correo = claims.get('sub')
        datos = request.json
        password = datos.get('password')

        if not password:
            return jsonify({"ok": False, "status": 400, "data": {"message": "Token y nueva contraseña son requeridos"}}), 400

        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        usuario.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
        usuario.cambiar_clave = False
        await usuario.save()

        await add_trazabilidad({
            'accion': f"Primer restablecimiento de contraseña del usuario: {usuario.nombre}",
            'usuario': usuario,
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.post('/upload-photo')
@jwt_required()
async def upload_photo():
    try:
        claims = get_jwt()
        correo = claims.get('sub')
        
        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        if 'file' not in request.files:
            return jsonify({"ok": False, "status": 400, "data": {"message": "No se encontró archivo"}}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"ok": False, "status": 400, "data": {"message": "No se seleccionó archivo"}}), 400

        if file and allowed_file(file.filename):
            # Create upload folder if it doesn't exist
            create_folder_if_not_exists(UPLOAD_FOLDER)
            
            # Generate secure filename using user ID
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"user_{usuario.id}.{file_extension}"
            filepath = path.join(UPLOAD_FOLDER, filename)
            
            # Remove old photo if exists
            if usuario.foto:
                old_filepath = path.join(UPLOAD_FOLDER, usuario.foto)
                if path.exists(old_filepath):
                    os.remove(old_filepath)
            
            # Save new photo
            file.save(filepath)
            
            # Update user record
            usuario.foto = filename
            await usuario.save()

            await add_trazabilidad({
                "accion": f"Subir foto de perfil: {filename}",
                "usuario": usuario,
                "modulo": "Usuarios",
                "nivel_alerta": 2
            })

            return jsonify({
                "ok": True, 
                "status": 200, 
                "data": {
                    "message": "Foto subida exitosamente",
                    "filename": filename
                }
            })
        else:
            return jsonify({"ok": False, "status": 400, "data": {"message": "Tipo de archivo no permitido"}}), 400

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.get('/photo/<filename>')
async def get_photo(filename):
    try:
        # Secure the filename
        filename = secure_filename(filename)
        filepath = path.join(UPLOAD_FOLDER, filename)
        
        if not path.exists(filepath):
            return jsonify({"ok": False, "status": 404, "data": {"message": "Foto no encontrada"}}), 404
            
        return send_file(filepath)
        
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@usr.delete('/delete-photo')
@jwt_required()
async def delete_photo():
    try:
        claims = get_jwt()
        correo = claims.get('sub')
        
        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        if usuario.foto:
            filepath = path.join(UPLOAD_FOLDER, usuario.foto)
            if path.exists(filepath):
                os.remove(filepath)
            
            usuario.foto = None
            await usuario.save()

            await add_trazabilidad({
                "accion": "Eliminar foto de perfil",
                "usuario": usuario,
                "modulo": "Usuarios",
                "nivel_alerta": 2
            })

            return jsonify({"ok": True, "status": 200, "data": {"message": "Foto eliminada exitosamente"}})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "No hay foto para eliminar"}}), 404

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
