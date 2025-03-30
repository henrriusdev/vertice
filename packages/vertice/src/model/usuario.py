from tortoise.models import Model
from tortoise import fields

class Usuario(Model):
    id = fields.IntField(pk=True)
    cedula = fields.CharField(max_length=20, unique=True)
    nombre = fields.CharField(max_length=255)
    correo = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    
    activo = fields.BooleanField(default=True)  # ✅ Permitir bloquear/reactivar
    ruta_foto = fields.CharField(max_length=255, null=True)  # ✅ Foto de perfil (almacenada en carpeta)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)  # ✅ Fecha de creación
    ultima_sesion = fields.DatetimeField(null=True)  # ✅ Último acceso/login

    rol = fields.ForeignKeyField("model.Rol", related_name="usuarios")

    class Meta:
        table = "usuarios"
        table_description = "Usuarios registrados en el sistema"
