from tortoise.models import Model
from tortoise import fields

class Docente(Model):
    usuario = fields.OneToOneField('models.Usuario', related_name='docente')
    titulo = fields.CharField(max_length=50, null=True)
    fecha_ingreso = fields.DateField(null=True)

    class Meta:
        table = "docentes"
        table_description = "Docente"
