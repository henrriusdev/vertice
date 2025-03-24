from tortoise import fields, models

class Rol(models.Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "roles"
        table_description = "Rol"