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
        print(datos)

        if not isinstance(datos, list) or len(datos) != 3:
            return jsonify({"ok": False, "status": 400, "data": {"message": "Debe proporcionar exactamente 3 preguntas y respuestas"}}), 400

        for item in datos:
            if not item.get("pregunta") or not item.get("respuesta"):
                return jsonify({"ok": False, "status": 400, "data": {"message": "Cada item debe tener pregunta y respuesta"}}), 400

        usuario = await get_usuario_por_correo(correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        # Eliminar preguntas existentes
        await PreguntaSeguridad.filter(usuario_id=usuario.id).delete()

        # Crear las nuevas preguntas
        for i, item in enumerate(datos):
            pregunta = PreguntaSeguridad(
                usuario_id=usuario.id,
                pregunta=item["pregunta"],
                respuesta=generate_password_hash(item["respuesta"], method="pbkdf2:sha256", salt_length=16),
                orden=i
            )
            await pregunta.save()

        # Actualizar estado en usuario
        usuario.pregunta_configurada = True
        await usuario.save()

        await add_trazabilidad({
            'accion': f"Configuración de preguntas de seguridad del usuario: {usuario.nombre}",
            'usuario': usuario,
            'fecha': datetime.now(),
            'modulo': "Usuarios",
            'nivel_alerta': 2
        })

        return jsonify({"ok": True, "status": 200, "data": "Preguntas de seguridad configuradas correctamente"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@preg.get('/obtener/<correo>')
async def obtener_pregunta(correo):
    try:
        usuario = await Usuario.get_or_none(correo=correo)
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        preguntas = await PreguntaSeguridad.filter(usuario_id=usuario.id).order_by('orden').all()
        if not preguntas:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no tiene preguntas de seguridad configuradas"}}), 404

        return jsonify({
            "ok": True, 
            "status": 200, 
            "data": {
                "preguntas": [{
                    "pregunta": p.pregunta,
                    "orden": p.orden
                } for p in preguntas]
            }
        })

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@preg.post('/verificar')
async def verificar_pregunta():
    try:
        datos = request.json
        if not datos.get("correo") or not datos.get("respuesta") or not isinstance(datos.get("orden"), int):
            return jsonify({"ok": False, "status": 400, "data": {"message": "Debe proporcionar correo, respuesta y orden"}}), 400

        usuario = await Usuario.get_or_none(correo=datos["correo"])
        if not usuario:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Usuario no encontrado"}}), 404

        pregunta = await PreguntaSeguridad.get_or_none(usuario_id=usuario.id, orden=datos["orden"])
        if not pregunta:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Pregunta de seguridad no encontrada"}}), 404

        if not pregunta.check_respuesta(datos["respuesta"]):
            return jsonify({"ok": False, "status": 400, "data": {"message": "Respuesta incorrecta"}}), 400

        return jsonify({"ok": True, "status": 200, "data": "Respuesta correcta"})

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
