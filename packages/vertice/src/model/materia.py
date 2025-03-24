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
    id_carrera = fields.ForeignKeyField('model.Carrera', related_name='materias')
    dia = fields.CharField(max_length=20, null=True)
    hora_inicio = fields.CharField(max_length=10, null=True)
    hora_fin = fields.CharField(max_length=10, null=True)
    dia2 = fields.CharField(max_length=20, null=True)
    hora_inicio2 = fields.CharField(max_length=10, null=True)
    hora_fin2 = fields.CharField(max_length=10, null=True)
    ciclo = fields.CharField(max_length=10)
    modalidad = fields.CharField(max_length=20, null=True)
    maximo = fields.IntField(null=True)
    id_docente = fields.ForeignKeyField('model.Usuario', related_name='materias', null=True)

    class Meta:
        table = "materias"
        table_description = "Materia"