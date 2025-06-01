from tortoise.models import Model
from tortoise import fields
from werkzeug.security import generate_password_hash, check_password_hash

class PreguntaSeguridad(Model):
    id = fields.IntField(pk=True)
    usuario = fields.ForeignKeyField("models.Usuario", related_name="pregunta_seguridad")
    pregunta = fields.CharField(max_length=255)
    respuesta = fields.CharField(max_length=255)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    def check_respuesta(self, respuesta: str) -> bool:
        return check_password_hash(self.respuesta, respuesta)

    class Meta:
        table = "pregunta_seguridad"
        table_description = "Pregunta de seguridad del usuario"
