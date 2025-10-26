from django.db import models

class OfertaElectiva(models.Model):
    oferta_electiva_id = models.AutoField(primary_key=True)
    electiva = models.ForeignKey('Electiva', on_delete=models.CASCADE)
    #materia_id = models.ForeignKey('Materia', on_delete=models.CASCADE)
    periodo = models.IntegerField(null=False) # Ejemplo: 202401 para el primer semestre de 2024
    es_activa = models.BooleanField(default=True) # True si la oferta está activa, False si está inactiva
    
    def __str__(self):
        return f"OfertaElectiva {self.oferta_electiva_id} - Electiva {self.electiva} - Periodo {self.periodo}"