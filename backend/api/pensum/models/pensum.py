from django.db import models
from django.db.models import Sum

class Pensum(models.Model):
    pensum_id = models.AutoField(primary_key=True)
    programa_id = models.ForeignKey('Programa', on_delete=models.CASCADE) # FK a la tabla Programa
    anio_creacion = models.IntegerField(null=True) # Año de creación del pensum, por ejemplo, 2024 y puede ser null, no es obligatoria
    es_activo = models.BooleanField(default=True) # True si el pensum está activo, False si está inactivo
    # Este campo ya que será calculado automáticamente
    # creditos_obligatorios_totales = models.IntegerField(null=True) # Total de créditos obligatorios del pensum
    
    @property
    def creditos_obligatorios_totales(self):
        """Calcula automáticamente los créditos obligatorios hasta el semestre límite"""
        from api.materia.models.materia import Materia
        from api.configuracion.models.configuracion_elegibilidad import ConfiguracionElegibilidad

        materias = Materia.objects.filter(
            pensum_id=self,
            es_obligatoria=True,
            es_activa=True
        )

        config = ConfiguracionElegibilidad.get_config_activa(self.programa_id)
        semestre_limite = getattr(config, 'semestre_limite_electivas', None)
        if semestre_limite:
            materias = materias.filter(semestre__lte=semestre_limite)

        total = materias.aggregate(total_creditos=Sum('creditos'))['total_creditos']
        return total or 0
    
    @property
    def total_materias_obligatorias(self):
        """Cuenta el total de materias obligatorias activas"""
        from api.materia.models.materia import Materia
        return Materia.objects.filter(
            pensum_id=self,
            es_obligatoria=True,
            es_activa=True
        ).count()
    
    @property
    def total_materias_electivas(self):
        """Cuenta el total de materias electivas activas"""
        from api.materia.models.materia import Materia
        return Materia.objects.filter(
            pensum_id=self,
            es_obligatoria=False,
            es_activa=True
        ).count()
    
    @property
    def total_creditos_electivas(self):
        """Cuenta el total de créditos de materias electivas activas"""
        from api.materia.models.materia import Materia
        total = Materia.objects.filter(
            pensum_id=self,
            es_obligatoria=False,
            es_activa=True
        ).aggregate(total_creditos=Sum('creditos'))['total_creditos']
        return total or 0
    
    def __str__(self):
        return f"Pensum {self.pensum_id} - Programa {self.programa_id} - Año {self.anio_creacion}"