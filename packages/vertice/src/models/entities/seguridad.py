class Seguridad():
    def __init__(self, se_id, administracion, control_estudio) -> None:
        self.administracion = administracion
        self.control_estudio = control_estudio
        self.id = se_id

    def to_JSON(self):
        return {
            
            "id": self.id,
            "administracion": self.administracion,
            "control_estudio": self.control_estudio,
        }