from tortoise import fields, models

class Usuario(models.Model):
    id = fields.IntField(pk=True)
    cedula = fields.CharField(max_length=20, unique=True)
    fullname = fields.CharField(max_length=150)
    correo = fields.CharField(max_length=150)
    telefono = fields.CharField(max_length=20)
    password = fields.CharField(max_length=200)
    rol = fields.ForeignKeyField('model.Rol', related_name='usuarios')

    class Meta:
        table = "usuarios"
        table_description = "Usuario"