from django.db import models

class Materia(models.Model):
    materia_id = models.AutoField(primary_key=True)
    pensum_id = models.ForeignKey('Pensum', on_delete=models.CASCADE) # FK a la tabla Pensum
    nombre_materia = models.CharField(max_length=100, null=False)
    creditos = models.IntegerField(null=False)
    es_obligatoria = models.BooleanField(default=True) # True si es obligatoria, False si es electiva
    es_activa = models.BooleanField(default=True) # True si la materia está activa, False si está inactiva
    semestre = models.IntegerField(null=False) # Semestre en el que se imparte la materia
    def __str__(self):
        return self.nombre_materia