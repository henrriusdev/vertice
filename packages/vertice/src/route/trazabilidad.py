from flask import Blueprint, jsonify
from src.service.trazabilidad import get_trazabilidad

trz = Blueprint('trazabilidad_blueprint', __name__)

@trz.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@trz.get('/')
async def list_trazabilidad():
    try:
        data = await get_trazabilidad()
        return jsonify({"ok": True, "status": 200, "data": data})
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
