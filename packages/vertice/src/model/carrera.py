from tortoise.models import Model
from tortoise import fields

class Carrera(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=255)

    class Meta:
        table = "carreras"
        table_description = "Carrera"