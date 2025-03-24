from tortoise.models import Model
from tortoise import fields

class Monto(Model):
  id = fields.IntField(pk=True)
  concepto = fields.CharField(max_length=100)
  monto = fields.DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    table = "montos"
    table_description = "Monto"
