from django.contrib import admin
from api.configuracion.models.configuracion_elegibilidad import ConfiguracionElegibilidad

# Register your models here.

@admin.register(ConfiguracionElegibilidad)
class ConfiguracionElegibilidadAdmin(admin.ModelAdmin):
    list_display = ('configuracion_id', 'programa_id', 'porcentaje_avance_minimo', 'nota_aprobatoria', 
                    'semestre_limite_electivas', 'es_activo', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('es_activo', 'programa_id', 'fecha_creacion')
    search_fields = ('programa_id__nombre_programa',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Información General', {
            'fields': ('programa_id', 'es_activo')
        }),
        ('Configuración de Elegibilidad', {
            'fields': ('porcentaje_avance_minimo', 'nota_aprobatoria', 'semestre_limite_electivas', 
                      'niveles_creditos_periodos')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
