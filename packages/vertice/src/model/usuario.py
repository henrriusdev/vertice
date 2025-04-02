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

    rol = fields.ForeignKeyField("models.Rol", related_name="usuarios")
    
    def to_dict(self):
        
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombre": self.nombre,
            "correo": self.correo,
            "activo": self.activo,
            "ruta_foto": self.ruta_foto,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "ultima_sesion": self.ultima_sesion.isoformat() if self.ultima_sesion else None,
            "rol": {
                "id": self.rol.id if self.rol else None,
                "nombre": self.rol.nombre if self.rol else None,
            }
        }

    class Meta:
        table = "usuarios"
        table_description = "Usuarios registrados en el sistema"
