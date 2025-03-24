from service.seguridadmodel import SeguridadModel
from flask import Blueprint, jsonify

seg_bp = Blueprint('seg_bp', __name__)

@seg_bp.route('/admin', methods=['GET'])
def get_admin():
    try:
        admin = SeguridadModel.get_clave_admin()
        return jsonify({
            'ok': True,
            'status': 200,
            'data': {'admin': admin}
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'ok': False,
            'status': 500,
            'message': str(e)
        }), 500


@seg_bp.route("/control", methods=["GET"])
def get_control():
    try:
        admin = SeguridadModel.get_clave_control()
        return jsonify({
            'ok': True,
            'status': 200,
            'data': {'control': admin}
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'ok': False,
            'status': 500,
            'message': str(e)
        }), 500

