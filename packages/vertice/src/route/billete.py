from flask import Blueprint, jsonify, request
from src.service.billetes import get_billetes, get_billete, add_billete, update_billete

bil = Blueprint("billete_blueprint", __name__)

@bil.route('/')
async def get_all():
    data = await get_billetes()
    return jsonify({"ok": True, "status": 200, "data": data})

@bil.route('/<int:id>')
async def get_one(id):
    data = await get_billete(id)
    return jsonify({"ok": True, "status": 200, "data": data})

@bil.route('/add', methods=['POST'])
async def add():
    payload = request.json
    await add_billete(payload)
    return jsonify({"ok": True, "status": 200})

@bil.route('/update/<int:id>', methods=['PUT'])
async def update(id):
    payload = request.json
    await update_billete(id, payload)
    return jsonify({"ok": True, "status": 200})