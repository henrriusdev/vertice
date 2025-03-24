from flask import Blueprint, jsonify, request
from service.entities.docente import Docente
from service.docentemodel import DocenteModel
from service.materiamodel import MateriaModel
from service.entities.materias import Materias
from packages.vertice.src.service.trazabilidad import TrazabilidadModel
from service.entities.trazabilidad import Trazabilidad
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime

doc = Blueprint('docentes_blueprint', __name__)

@doc.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@doc.route('/')
@jwt_required()
def get_docentes():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        docentes = DocenteModel.get_docentes()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener Docentes",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Docentes",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": docentes})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@doc.route('/<cedula>')
@jwt_required()
def get_docente(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        docente = DocenteModel.get_docente(cedula)
        
        if docente != None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener Docente con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Docentes",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": docente})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "docente no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@doc.route('/peticiones/<cedula>')
@jwt_required()
def get_peticiones_por_docente(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        peticiones = DocenteModel.get_peticiones_por_docente(cedula)

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion=f"Obtener Peticiones del Docente con cédula: {cedula}",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Docentes",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": peticiones})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@doc.route('/add', methods=["POST"])
@jwt_required()
def add_docente():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        docente = Docente(str(cedula), fullname, correo, telefono, password)
        affected_rows = DocenteModel.add_docente(docente)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir Docente con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Docentes",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@doc.route('/update/<cedula>', methods=["PUT"])
@jwt_required()
def update_docente(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        docente = Docente(str(cedula), fullname, correo, telefono, password)
        affected_rows = DocenteModel.update_docente(docente)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar Docente con cédula: {cedula}, nombre: {fullname}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Docentes",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@doc.route('/delete/<cedula>', methods=["DELETE"])
@jwt_required()
def delete_docente(cedula):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        docente = Docente(str(cedula))
        affected_rows = DocenteModel.delete_docente(docente)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar Docente con cédula: {cedula}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Docentes",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "docente no encontrado"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@doc.route("/upload", methods=["PATCH"])
def modificar_materia_estudiante():
    try:
        cedula_estudiante = request.json.get('cedula_estudiante')
        nombre_campo = request.json.get('nombre_campo')
        valor = request.json.get('valor')
        materia = request.json.get('materia')
        
        message = MateriaModel.modificar_materia_estudiante(materia, cedula_estudiante, nombre_campo, valor)

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion=f"Modificar materia del estudiante con cédula: {cedula_estudiante}, campo: {nombre_campo}, valor: {valor}",
            usuario=materia,
            fecha=datetime.now(),
            modulo="Materias",
            nivel_alerta=2
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": None}), 200
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@doc.route('/login', methods=["POST"])
def login_docente():
    try:
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        docente = Docente(correo=usuario)
        docente = DocenteModel.login(docente)
        if docente is not None:
            if check_password_hash(docente.password, clave):
                access_token = create_access_token(identity=docente.correo, expires_delta=timedelta(hours=2), additional_claims={'rol': 'D', 'nombre': docente.fullname})
                
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Inicio de sesión del docente con cédula: {docente.cedula}",
                    usuario=docente.correo,
                    fecha=datetime.now(),
                    modulo="Autenticacion",
                    nivel_alerta=1
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": {"docente": docente.to_JSON(), "access_token": f"Bearer {access_token}"}})
            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@doc.route('/refresh')
@jwt_required()
def jwt_docente():
    try:
        correo_docente = get_jwt_identity()  # Esto obtiene la identidad del token, en este caso, un correo
        docente: Docente | None  # Declaramos sin iniciar la variable del docente
        if correo_docente is not None:
            docente_entity = Docente(correo=correo_docente)  # Creamos la entidad del docente
            docente = DocenteModel.login(docente_entity)  # Revisamos la bd
            if docente != None:
                return jsonify({"ok": True, "status": 200, "data": docente.to_JSON()})  # Retornamos si es correcto
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "no autorizado"}}), 401
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@doc.route('/update-password', methods=["PATCH"])
@jwt_required()
def update_password():
    try:
        claims = get_jwt()
        usuario = claims.get('sub')
        nombre = claims.get('nombre')
        
        current_password = request.json['current_password']
        new_password = request.json['new_password']

        docente = DocenteModel.get_docente_by_correo(usuario)
        if docente and check_password_hash(docente.password, current_password):
            new_password = generate_password_hash(new_password, method="sha256")
            affected_rows = DocenteModel.update_password(usuario, new_password)
            if affected_rows == 1:
                # Registrar trazabilidad
                trazabilidad = Trazabilidad(
                    accion=f"Actualizar contraseña del docente: {nombre}",
                    usuario=usuario,
                    fecha=datetime.now(),
                    modulo="Docentes",
                    nivel_alerta=2
                )
                TrazabilidadModel.add_trazabilidad(trazabilidad)

                return jsonify({"ok": True, "status": 200, "data": "Contraseña actualizada exitosamente"})
            else:
                return jsonify({"ok": False, "status": 500, "data": "Error al actualizar la contraseña"}), 500
        else:
            return jsonify({"ok": False, "status": 401, "data": "Contraseña actual incorrecta"}), 401
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
    

@doc.route('/reiniciar/<correo>', methods = ['POST'])
@jwt_required()
def reiniciar_clave(correo):
    try:
        correo_coord = get_jwt_identity()
        claims = get_jwt()
        nombre = claims.get('nombre')
        docente: Docente | None
        if correo is not None:
            docente = DocenteModel.get_docente_by_correo(correo)
            if docente != None:
                cedula = docente.cedula.split('-')[1]
                new_password = generate_password_hash(cedula, method="sha256")
                affected_rows = DocenteModel.update_password(correo, new_password)
                if affected_rows == 1:
                    # Registrar trazabilidad
                    trazabilidad = Trazabilidad(
                        accion=f"Reiniciar contraseña del docente: {docente.fullname}",
                        usuario=correo_coord,
                        fecha=datetime.now(),
                        modulo="Docentes",
                        nivel_alerta=2
                    )
                    TrazabilidadModel.add_trazabilidad(trazabilidad)

                    return jsonify({"ok": True, "status": 200, "data": "Contraseña reiniciada exitosamente"})
            else:
                return jsonify({"ok": False, "status": 500, "data": "Error al reiniciar la contraseña"}), 500
        else:
            return jsonify({"ok": False, "status": 401, "data": "Contraseña actual incorrecta"}), 401
    except Exception as ex:
        print(ex)
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

            