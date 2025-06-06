from tortoise.models import Model
from tortoise import fields
from werkzeug.security import generate_password_hash, check_password_hash
from tortoise.exceptions import ValidationError

class PreguntaSeguridad(Model):
    id = fields.IntField(pk=True)
    usuario = fields.ForeignKeyField("models.Usuario", related_name="preguntas_seguridad")
    pregunta = fields.CharField(max_length=255)
    respuesta = fields.CharField(max_length=255)
    orden = fields.IntField()
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    def check_respuesta(self, respuesta: str) -> bool:
        return check_password_hash(self.respuesta, respuesta)

    async def save(self, *args, **kwargs) -> None:
        # Verificar que el usuario no tenga más de 3 preguntas
        if not self.id:  # Solo al crear
            count = await PreguntaSeguridad.filter(usuario_id=self.usuario_id).count()
            if count >= 3:
                raise ValidationError('El usuario ya tiene 3 preguntas de seguridad')
            
            # Asignar orden automáticamente
            self.orden = count

        await super().save(*args, **kwargs)

    class Meta:
        table = "pregunta_seguridad"
        table_description = "Preguntas de seguridad del usuario"
        unique_together = ("usuario", "orden")
