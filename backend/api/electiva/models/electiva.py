from django.db import models

class Electiva(models.Model):
    electiva_id = models.AutoField(primary_key=True)
    programa_id = models.ForeignKey('Programa', on_delete=models.CASCADE)
    nombre_electiva = models.CharField(max_length=100, null=False)
    es_activa = models.BooleanField(default=True) # True si la electiva está activa, False si está inactiva

    def __str__(self):
        return self.nombre_electiva