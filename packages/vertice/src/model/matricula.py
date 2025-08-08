from tortoise import fields
from tortoise.models import Model

class Matricula(Model):
    id = fields.IntField(pk=True)
    cod_materia = fields.ForeignKeyField("models.Materia", related_name='matriculas')
    cedula_estudiante = fields.ForeignKeyField("models.Estudiante", related_name='matriculas')
    asignacion = fields.ForeignKeyField("models.AsignacionMateria", related_name='matriculas', null=True)
    notas = fields.JSONField()
    uc = fields.IntField()
    ciclo = fields.CharField(max_length=10)

    class Meta:
        table = "matriculas"
        table_description = "Matricula"
        unique_together = ("cod_materia", "cedula_estudiante", "ciclo")