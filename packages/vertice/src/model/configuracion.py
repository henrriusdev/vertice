from tortoise.models import Model
from tortoise import fields

class Configuracion(Model):
    id = fields.IntField(pk=True)
    ciclo = fields.CharField(max_length=10)
    num_porcentaje = fields.IntField(default=3)  # cuántas divisiones de nota tiene el ciclo
    num_cuotas = fields.IntField(default=5)     # cuántas cuotas tendrá el ciclo
    horario_inicio = fields.DatetimeField()
    horario_fin = fields.DatetimeField()
    cuotas = fields.JSONField(null=True)  # fechas de cuotas dinámicas
    porcentajes = fields.JSONField(null=True)  # porcentajes de notas del ciclo

    class Meta:
        table = "configuraciones"
        table_description = "Configuración"