from tortoise import fields
from tortoise.models import Model

class Estudiante(Model):
    usuario = fields.OneToOneField('models.Usuario', related_name='estudiante')
    semestre = fields.IntField()
    carrera = fields.ForeignKeyField("models.Carrera", related_name='estudiantes')
    promedio = fields.DecimalField(max_digits=10, decimal_places=2)
    direccion = fields.CharField(max_length=300)
    fecha_nac = fields.DatetimeField()
    edad = fields.IntField()
    sexo = fields.CharField(max_length=20)

    class Meta:
        table = "estudiantes"
        table_description = "Estudiante"