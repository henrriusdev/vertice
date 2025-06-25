from tortoise import fields
from tortoise.models import Model

class Materia(Model):
    id = fields.CharField(pk=True, max_length=15)
    nombre = fields.CharField(max_length=100)
    prelacion = fields.CharField(max_length=250)
    unidad_credito = fields.IntField()
    hp = fields.IntField()
    ht = fields.IntField()
    semestre = fields.IntField()
    id_carrera = fields.ForeignKeyField("models.Carrera", related_name='materias')
    horarios = fields.JSONField(null=True)  # Nuevo campo agrupado
    maximo = fields.IntField(null=True)
    id_docente = fields.ForeignKeyField("models.Docente", related_name='materias', null=True)

    class Meta:
        table = "materias"
        table_description = "Materia"
