from tortoise.models import Model
from tortoise import fields

class Pago(Model):
    id = fields.IntField(pk=True)
    cedula_estudiante = fields.ForeignKeyField('model.Estudiante', related_name='pagos')
    metodo_pago = fields.ForeignKeyField('model.MetodoPago', related_name='pagos')
    monto = fields.DecimalField(max_digits=12, decimal_places=2)
    concepto = fields.CharField(max_length=100)
    fecha_pago = fields.DatetimeField()
    referencia_transferencia = fields.CharField(max_length=50, null=True)
    ciclo = fields.CharField(max_length=10)


    class Meta:
      table = "montos"
      table_description = "Monto"
