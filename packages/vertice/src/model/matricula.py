from tortoise import fields
from tortoise.models import Model

class Matricula(Model):
    id = fields.IntField(pk=True)
    cod_materia = fields.ForeignKeyField('model.Materia', related_name='matriculas')
    cedula_estudiante = fields.ForeignKeyField('model.Estudiante', related_name='matriculas')
    notas = fields.JSONField()
    uc = fields.IntField()
    ciclo = fields.CharField(max_length=10)

    class Meta:
        table = "matriculas"
        table_description = "Matricula"
        unique_together = ("cod_materia", "cedula_estudiante", "ciclo")