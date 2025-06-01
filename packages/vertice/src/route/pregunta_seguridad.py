import traceback
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash

from src.middleware.sesion import unica_sesion_requerida
from src.model.pregunta_seguridad import PreguntaSeguridad
from src.model.usuario import Usuario
from src.service.trazabilidad import add_trazabilidad
from src.service.usuarios import get_usuario_por_correo

preg = Blueprint('pregunta_seguridad_blueprint', __name__)

@preg.post('/configurar')
@jwt_required()
@unica_sesion_requerida
async def configurar_pregunta():
    try:
        claims = get_jwt()
        correo = claims.get('sub')
        datos = request.json

        if not datos.get("pregunta") or not datos.get("respuesta"):
            return jsonify({"ok": False, "status": 400, "data": {"message": "Debe proporcionar pregunta y respuesta"}}), 400

        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        # Si ya existe una pregunta, actualizarla
        pregunta_existente = await PreguntaSeguridad.filter(usuario_id=usuario.id).first()
        if pregunta_existente:
            pregunta_existente.pregunta = datos["pregunta"]
            pregunta_existente.respuesta = generate_password_hash(datos["respuesta"], method="pbkdf2:sha256", salt_length=16)
            await pregunta_existente.save()
        else:
            # Crear nueva pregunta
            await PreguntaSeguridad.create(
                usuario_id=usuario.id,
                pregunta=datos["pregunta"],
                respuesta=generate_password_hash(datos["respuesta"], method="pbkdf2:sha256", salt_length=16)
            )

        # Actualizar estado en usuario
        usuario.pregunta_configurada = True
        await usuario.save()

        await add_trazabilidad({
            'accion': f"Configuración de pregunta de seguridad del usuario: {usuario.nombre}",
            'usuario': usuario,
            'fecha': datetime.now(),
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Pregunta de seguridad configurada correctamente"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@preg.get('/obtener/<correo>')
async def obtener_pregunta(correo):
    try:
        usuario = await Usuario.get_or_none(correo=correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        pregunta = await PreguntaSeguridad.get_or_none(usuario_id=usuario.id)
        if not pregunta:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no tiene pregunta de seguridad configurada"}}), 404

        return jsonify({
            "ok": True, 
            "status": 200, 
            "data": {
                "pregunta": pregunta.pregunta
            }
        })

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@preg.post('/verificar')
async def verificar_pregunta():
    try:
        datos = request.json
        if not datos.get("correo") or not datos.get("respuesta"):
            return jsonify({"ok": False, "status": 400, "data": {"message": "Debe proporcionar correo y respuesta"}}), 400

        usuario = await Usuario.get_or_none(correo=datos["correo"])
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        pregunta = await PreguntaSeguridad.get_or_none(usuario_id=usuario.id)
        if not pregunta:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no tiene pregunta de seguridad configurada"}}), 404

        if not pregunta.check_respuesta(datos["respuesta"]):
            return jsonify({"ok": False, "status": 400, "data": {"message": "Respuesta incorrecta"}}), 400

        return jsonify({"ok": True, "status": 200, "data": "Respuesta correcta"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
