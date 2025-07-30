from tortoise import fields
from tortoise.models import Model

class Coordinador(Model):
    usuario = fields.OneToOneField('models.Usuario', related_name='coordinador')
    carrera = fields.ForeignKeyField("models.Carrera", related_name='coordinadores')
    telefono = fields.CharField(max_length=20)
    activo = fields.BooleanField(default=True)  # Para borrado lógico

    class Meta:
        table = "coordinadores"
        table_description = "Coordinación"