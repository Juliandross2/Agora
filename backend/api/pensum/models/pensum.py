from django.db import models

class Pensum(models.Model):
    pensum_id = models.AutoField(primary_key=True)
    programa_id = models.ForeignKey('Programa', on_delete=models.CASCADE) # FK a la tabla Programa
    anio_creacion = models.IntegerField(null=True) # Año de creación del pensum, por ejemplo, 2024 y puede ser null, no es obligatoria
    es_activo = models.BooleanField(default=True) # True si el pensum está activo, False si está inactivo

    def __str__(self):
        return f"Pensum {self.pensum_id} - Programa {self.programa_id} - Año {self.anio_creacion}"