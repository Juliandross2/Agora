from django.db import models

class Programa(models.Model):
    programa_id = models.AutoField(primary_key=True)
    nombre_programa = models.CharField(max_length=100, null=False)
    es_activo = models.BooleanField(default=True) # True si el programa está activo, False si está inactivo

    def __str__(self):
        return self.nombre_programa