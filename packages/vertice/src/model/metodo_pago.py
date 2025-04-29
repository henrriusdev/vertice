from tortoise.models import Model
from tortoise import fields


class MetodoPago(Model):
  id = fields.IntField(pk=True)
  nombre = fields.CharField(max_length=50, unique=True)
  
  
  def to_dict(self):
    return {
      "id": self.id,
      "nombre": self.nombre
    }
  
  class Meta:
    table = "metodos_pago"
    table_description = "Metodo de pago"

