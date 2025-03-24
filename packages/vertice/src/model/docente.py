from tortoise.models import Model
from tortoise import fields

class Docente(Model):
    usuario = fields.OneToOneField('model.Usuario', related_name='docente')

    class Meta:
        table = "docentes"
        table_description = "Docente"