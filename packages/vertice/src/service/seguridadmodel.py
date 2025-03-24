from database.db import get_connection
class SeguridadModel():
    
    @classmethod
    def get_clave_admin(cls):

        connection = get_connection()

        with connection.cursor() as cursor: 
            cursor.execute("SELECT administracion FROM seguridad WHERE id = 1;")
            current_number = cursor.fetchone()
            current_number = current_number[0]
        connection.close()
        return current_number
    

    @classmethod
    def get_clave_control(cls):

        connection = get_connection()

        with connection.cursor() as cursor: 
            cursor.execute("SELECT control_estudio FROM seguridad WHERE id = 1;")
            current_number = cursor.fetchone()
            current_number = current_number[0]
        connection.close()
        return current_number