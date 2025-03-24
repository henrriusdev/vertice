from flask import Blueprint, jsonify
from service.factura import get_incremented_number

factura_bp = Blueprint("factura_bp", __name__)

@factura_bp.route('/', methods=['GET'])
async def get_invoice():
    nro = await get_incremented_number()
    return jsonify({"ok": True, "status": 200, "data": {"nroFactura": nro}})