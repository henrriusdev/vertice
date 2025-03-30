from tortoise import fields
from tortoise.models import Model

class Trazabilidad(Model):
    id = fields.IntField(pk=True)
    accion = fields.CharField(max_length=300)
    usuario = fields.ForeignKeyField("models.Usuario", related_name='trazabilidad')
    fecha = fields.DatetimeField()
    modulo = fields.CharField(max_length=50)
    nivel_alerta = fields.IntField(null=True)

    class Meta:
        table = "trazabilidad"
        table_description = "Trazabilidad"