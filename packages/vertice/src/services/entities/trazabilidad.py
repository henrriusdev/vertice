class Trazabilidad():
    def __init__(self, id=None, accion=None, usuario=None, fecha=None, modulo=None, nivel_alerta=None):
        self.id = id
        self.accion = accion
        self.usuario = usuario
        self.fecha = fecha
        self.modulo = modulo
        self.nivel_alerta = nivel_alerta
    
    def to_JSON(self):
        return {
            "id": self.id,
            "accion": self.accion,
            "usuario": self.usuario,
            "fecha": self.fecha,
            "modulo": self.modulo,
            "nivel_alerta": self.nivel_alerta
        }
