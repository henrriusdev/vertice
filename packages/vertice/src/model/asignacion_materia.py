from tortoise import fields
from tortoise.models import Model

class AsignacionMateria(Model):
    id = fields.IntField(pk=True)
    materia = fields.ForeignKeyField("models.Materia", related_name='asignaciones')
    profesor = fields.ForeignKeyField("models.Docente", related_name='asignaciones')
    horarios = fields.JSONField()
    nombre = fields.CharField(max_length=15)

    class Meta:
        table = "asignacion_materia"
        table_description = "Asignación de Profesor y Horarios a Materia"