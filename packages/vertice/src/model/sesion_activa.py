from tortoise import fields
from tortoise.models import Model

class SesionActiva(Model):
    id = fields.IntField(pk=True)
    usuario = fields.ForeignKeyField("models.Usuario", related_name="sesiones")
    jti = fields.CharField(max_length=255, unique=True)  # JWT ID
    creado_en = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "sesiones_activas"
        table_description = "Sesiones activas por usuario"
