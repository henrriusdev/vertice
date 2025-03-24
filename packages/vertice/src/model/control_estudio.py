from tortoise.models import Model
from tortoise import fields

class ControlEstudio(Model):
    usuario = fields.OneToOneField('models.Usuario', related_name='control')

    class Meta:
        table = "control_estudio"