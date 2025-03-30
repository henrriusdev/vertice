import asyncio
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.settings import settings
from src.database.db import init_db
from src.route import pagos, usuario, docente, carreras, materias, billete, coordinacion, peticiones, config, archivos, trazabilidad, sesiones, estudiantes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    JWTManager(app)
    init_db()

    # Blueprints
    blueprints = [
        (archivos.arc,     '/api/archivos'),
        (billete.bil,      '/api/billetes'),
        (carreras.car,     '/api/carreras'),
        (config.cfg,       '/api/config'),
        (coordinacion.crd, '/api/coordinacion'),
        (docente.doc,      '/api/docente'),
        (estudiantes.est,  '/api/estudiantes'),
        (materias.mat,     '/api/materias'),
        (pagos.pago,       '/api/pagos'),
        (peticiones.ptc,   '/api/peticiones'),
        (sesiones.ses,     '/api/sesiones'),
        (usuario.usr,      '/api/usuario'),
        (trazabilidad.trz, '/api/trazabilidad'),
    ]

    for bp, url in blueprints:
        app.register_blueprint(bp, url_prefix=url)

    app.register_error_handler(404, page_not_found)

    return app


def page_not_found(error):
    return jsonify({"ok": False, "status": 404, "data": {"message": "Page not found"}}), 404
