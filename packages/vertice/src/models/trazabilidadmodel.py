from models.entities.trazabilidad import Trazabilidad
from database.db import get_connection
from datetime import datetime

class TrazabilidadModel():

    @classmethod
    def add_trazabilidad(cls, trazabilidad: Trazabilidad):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO trazabilidad (accion, usuario, fecha, modulo, nivel_alerta)
                    VALUES (%s, %s, %s, %s, %s)
                """, (trazabilidad.accion, trazabilidad.usuario, trazabilidad.fecha, trazabilidad.modulo, trazabilidad.nivel_alerta))
                connection.commit()
                affected_rows = cursor.rowcount
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_trazabilidad(cls):
        try:
            connection = get_connection()
            trazabilidad_list = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM trazabilidad")
                result = cursor.fetchall()
                for row in result:
                    trazabilidad = Trazabilidad(id=row[0], accion=row[1], usuario=row[2], fecha=row[3], modulo=row[4], nivel_alerta=row[5])
                    trazabilidad_list.append(trazabilidad.to_JSON())
            connection.close()
            return trazabilidad_list
        except Exception as ex:
            raise Exception(ex)
