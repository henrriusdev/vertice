from tortoise import fields
from tortoise.models import Model

class Coordinador(Model):
    usuario = fields.OneToOneField('model.Usuario', related_name='coordinador')

    class Meta:
        table = "coordinadores"
        table_description = "Coordinación"