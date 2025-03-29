from tortoise import fields
from tortoise.models import Model

class Coordinador(Model):
    usuario = fields.OneToOneField('model.Usuario', related_name='coordinador')
    carrera = fields.ForeignKeyField('model.Carrera', related_name='coordinadores')
    telefono = fields.CharField(max_length=20)
    

    class Meta:
        table = "coordinadores"
        table_description = "Coordinación"