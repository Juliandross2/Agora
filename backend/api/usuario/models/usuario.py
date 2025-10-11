from django.db import models

class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100, null=False)
    email_usuario = models.EmailField(max_length=100, null=False, unique=True)
    es_activo = models.BooleanField(default=True) # True si el usuario está activo, False si está inactivo

    def __str__(self):
        return self.nombre_usuario