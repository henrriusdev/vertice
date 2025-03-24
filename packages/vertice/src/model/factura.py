from tortoise.models import Model
from tortoise import fields

class Factura(Model):
    id = fields.IntField(pk=True)
    numero = fields.CharField(max_length=50, unique=True)
    fecha_emision = fields.DatetimeField(auto_now_add=True)
    monto_total = fields.DecimalField(max_digits=12, decimal_places=2)
    pago = fields.ForeignKeyField('model.Pago', related_name='factura', null=True)

    class Meta:
        table = "facturas"
        table_description = "Factura"