from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from settings import settings
from database.db import init_db
from routes import pagos, students, usuario, docente, carreras, materias, billete, coordinacion, control, peticiones, config, files, generar, SuperUsuario, transferencia, factura, trazabilidad, seguridad

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY

    JWTManager(app)
    init_db(app)

    # Blueprints
    blueprints = [
        (students.main, '/api/students'),
        (pagos.pago, '/api/pagos'),
        (usuario.user, '/api/usuario'),
        (docente.doc, '/api/docente'),
        (carreras.carrera, '/api/carreras'),
        (materias.materia, '/api/materias'),
        (billete.billete, '/api/billetes'),
        (coordinacion.coordinacion, '/api/coordinacion'),
        (control.control, '/api/control'),
        (peticiones.peticion, '/api/peticiones'),
        (config.config, '/api/config'),
        (files.files, '/api/archivos'),
        (generar.generar_pdf, '/api/generar_ficha'),
        (SuperUsuario.superUs, '/api/superUsuario'),
        (transferencia.transf, '/api/transferencias'),
        (factura.factura_bp, '/api/factura'),
        (trazabilidad.tr, '/api/trazabilidad'),
        (seguridad.seg_bp, '/api/seguridad'),
    ]

    for bp, url in blueprints:
        app.register_blueprint(bp, url_prefix=url)

    app.register_error_handler(404, page_not_found)

    return app


def page_not_found(error):
    return jsonify({"ok": False, "status": 404, "data": {"message": "Page not found"}}), 404


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=settings.DEBUG)
