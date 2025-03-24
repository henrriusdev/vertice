from service.entities.trazabilidad import Trazabilidad
from packages.vertice.src.service.trazabilidad import TrazabilidadModel
from flask import Blueprint, jsonify

tr = Blueprint('tr_Blueprint', __name__)

@tr.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
  
@tr.get('/')
def get_trazabilidad():
    try:
        trazabilidad = TrazabilidadModel.get_trazabilidad()
        return jsonify({"ok": True, "status": 200, "data": trazabilidad})
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}), 500
      
