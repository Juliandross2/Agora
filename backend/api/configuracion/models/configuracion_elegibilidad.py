from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class ConfiguracionElegibilidad(models.Model):
    """
    Modelo para almacenar configuraciones de elegibilidad para cursar electivas.
    Cada programa académico debe tener su propia configuración activa.
    """
    configuracion_id = models.AutoField(primary_key=True)
    
    # Relación con Programa (requerido)
    programa_id = models.ForeignKey(
        'Programa',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='programa_id',
        help_text="Programa académico asociado (requerido)"
    )
    
    # Configuraciones principales
    porcentaje_avance_minimo = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0.60,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Porcentaje mínimo de avance requerido (0.60 = 60%)"
    )
    
    nota_aprobatoria = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=3.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Nota mínima para considerar una materia aprobada"
    )
    
    semestre_limite_electivas = models.IntegerField(
        default=7,
        validators=[MinValueValidator(1)],
        help_text="Hasta qué semestre se exige tener TODO aprobado"
    )
    
    # Reglas según niveles (almacenado como JSON)
    niveles_creditos_periodos = models.JSONField(
        default=dict,
        help_text="Reglas por nivel. Ejemplo: {8: {'min_creditos': 112, 'max_periodos': 7}}"
    )
    
    # Control de estado
    es_activo = models.BooleanField(
        default=True,
        help_text="True si esta configuración está activa"
    )
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'configuracion_elegibilidad'
        verbose_name = 'Configuración de Elegibilidad'
        verbose_name_plural = 'Configuraciones de Elegibilidad'
        app_label = 'api'
        # Solo una configuración activa por programa
        constraints = [
            models.UniqueConstraint(
                fields=['programa_id', 'es_activo'],
                condition=models.Q(es_activo=True),
                name='unique_active_config_per_program'
            )
        ]
        indexes = [
            models.Index(fields=['programa_id', 'es_activo']),
            models.Index(fields=['es_activo']),
        ]
    
    def __str__(self):
        programa = self.programa_id.nombre_programa
        estado = "Activo" if self.es_activo else "Inactivo"
        return f"Config {self.configuracion_id} - {programa} ({estado})"
    
    def to_dict(self):
        """Convierte el modelo a un diccionario compatible con CONFIG"""
        return {
            "porcentaje_avance_minimo": float(self.porcentaje_avance_minimo),
            "nota_aprobatoria": float(self.nota_aprobatoria),
            "semestre_limite_electivas": self.semestre_limite_electivas,
            "niveles_creditos_periodos": self.niveles_creditos_periodos if self.niveles_creditos_periodos else {}
        }
    
    @classmethod
    def get_config_activa(cls, programa_id):
        """
        Obtiene la configuración activa para un programa específico.
        Si no existe, retorna None.
        
        Args:
            programa_id: ID del programa (requerido)
            
        Returns:
            ConfiguracionElegibilidad o None
        """
        if not programa_id:
            return None
            
        return cls.objects.filter(
            programa_id=programa_id,
            es_activo=True
        ).first()

