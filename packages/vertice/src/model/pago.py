from tortoise.models import Model
from tortoise import fields

class Pago(Model):
    id = fields.IntField(pk=True)
    cedula_estudiante = fields.ForeignKeyField("models.Estudiante", related_name='pagos')
    metodo_pago = fields.ForeignKeyField("models.MetodoPago", related_name='pagos')
    monto = fields.DecimalField(max_digits=12, decimal_places=2)
    concepto = fields.CharField(max_length=100)
    fecha_pago = fields.DatetimeField()
    referencia_transferencia = fields.CharField(max_length=50, null=True)
    ciclo = fields.CharField(max_length=10)
    tasa_divisa = fields.DecimalField(max_digits=12, decimal_places=2, null=True)
    activo = fields.BooleanField(default=True)  # Para borrado lógico

    class Meta:
      table = "pagos"
      table_description = "Monto"
