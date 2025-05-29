from tortoise.models import Model
from tortoise import fields

class Billete(Model):
  id = fields.IntField(pk=True)
  serial = fields.CharField(max_length=100)
  monto = fields.DecimalField(max_digits=10, decimal_places=2)
  pago = fields.OneToOneField("models.Pago", related_name='billete', on_delete=fields.CASCADE)

  class Meta:
    table = "billetes"
    table_description = "Billete"