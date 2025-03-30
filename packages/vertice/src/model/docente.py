from tortoise.models import Model
from tortoise import fields

class Docente(Model):
    usuario = fields.OneToOneField('models.Usuario', related_name='docente')
    titulo = fields.CharField(max_length=50, null=True)
    dedicacion = fields.CharField(max_length=50, null=True)
    especialidad = fields.CharField(max_length=100, null=True)
    estatus = fields.CharField(max_length=20, default="Activo")
    fecha_ingreso = fields.DateField(null=True)
    observaciones = fields.TextField(null=True)

    class Meta:
        table = "docentes"
        table_description = "Docente"
