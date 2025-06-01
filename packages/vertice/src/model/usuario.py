from tortoise.models import Model
from tortoise import fields

class Usuario(Model):
    id = fields.IntField(pk=True)
    cedula = fields.CharField(max_length=20, unique=True)
    nombre = fields.CharField(max_length=255)
    correo = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    
    activo = fields.BooleanField(default=True)  # ✅ Permitir bloquear/reactivar
    fecha_creacion = fields.DatetimeField(auto_now_add=True)  # ✅ Fecha de creación
    pregunta_configurada = fields.BooleanField(default=False)  # ✅ Indica si tiene pregunta de seguridad

    rol = fields.ForeignKeyField("models.Rol", related_name="usuarios")
    
    def to_dict(self):
        cedula = self.cedula.replace("V-", "").replace("E-", "")
        cambiar_clave = self.check_password(cedula)
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombre": self.nombre,
            "correo": self.correo,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.strftime("%d/%m/%Y") if self.fecha_creacion else None,
            "cambiar_clave": cambiar_clave,
            "pregunta_configurada": self.pregunta_configurada,
            "rol": {
                "id": self.rol.id if self.rol else None,
                "nombre": self.rol.nombre if self.rol else None,
            },
        }

    def check_password(self, password: str) -> bool:
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

    class Meta:
        table = "usuarios"
        table_description = "Usuarios registrados en el sistema"
