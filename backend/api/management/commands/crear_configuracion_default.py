"""
Comando de gestión para crear una configuración por defecto de elegibilidad.

Uso:
    python manage.py crear_configuracion_default
    python manage.py crear_configuracion_default --programa_id 1
"""
from django.core.management.base import BaseCommand
from api.historias.models.configuracion_elegibilidad import ConfiguracionElegibilidad
from api.historias.config.config import CONFIG


class Command(BaseCommand):
    help = 'Crea una configuración por defecto de elegibilidad en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--programa_id',
            type=int,
            help='ID del programa para crear configuración específica (opcional)',
        )
        parser.add_argument(
            '--desactivar_otras',
            action='store_true',
            help='Desactiva otras configuraciones activas del mismo programa',
        )

    def handle(self, *args, **options):
        programa_id = options.get('programa_id')
        desactivar_otras = options.get('desactivar_otras', False)

        # Si se especifica programa_id, verificar que existe
        programa = None
        if programa_id:
            try:
                from api.programa.models.programa import Programa
                programa = Programa.objects.get(programa_id=programa_id)
                self.stdout.write(
                    self.style.SUCCESS(f'Programa encontrado: {programa.nombre_programa}')
                )
            except Programa.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Programa con ID {programa_id} no existe')
                )
                return

        # Desactivar otras configuraciones si se solicita
        if desactivar_otras:
            configs_anteriores = ConfiguracionElegibilidad.objects.filter(
                programa_id=programa_id if programa_id else None,
                es_activo=True
            )
            count = configs_anteriores.update(es_activo=False)
            if count > 0:
                self.stdout.write(
                    self.style.WARNING(f'Se desactivaron {count} configuración(es) anterior(es)')
                )

        # Verificar si ya existe una configuración activa
        config_existente = ConfiguracionElegibilidad.get_config_activa(programa_id=programa_id)
        if config_existente:
            self.stdout.write(
                self.style.WARNING(
                    f'Ya existe una configuración activa para {"el programa" if programa_id else "configuración global"}. '
                    f'ID: {config_existente.configuracion_id}'
                )
            )
            respuesta = input('¿Desea crear otra configuración? (s/n): ')
            if respuesta.lower() != 's':
                self.stdout.write(self.style.SUCCESS('Operación cancelada'))
                return

        # Crear nueva configuración con valores por defecto
        nueva_config = ConfiguracionElegibilidad(
            programa_id=programa,
            porcentaje_avance_minimo=CONFIG['porcentaje_avance_minimo'],
            nota_aprobatoria=CONFIG['nota_aprobatoria'],
            semestre_limite_electivas=CONFIG['semestre_limite_electivas'],
            total_creditos_obligatorios=CONFIG['total_creditos_obligatorios'],
            niveles_creditos_periodos=CONFIG.get('niveles_creditos_periodos', {}),
            es_activo=True
        )
        nueva_config.save()

        tipo_config = f"para el programa '{programa.nombre_programa}'" if programa else "global"
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Configuración {tipo_config} creada exitosamente (ID: {nueva_config.configuracion_id})'
            )
        )
        self.stdout.write(f'  - Porcentaje avance mínimo: {nueva_config.porcentaje_avance_minimo * 100}%')
        self.stdout.write(f'  - Nota aprobatoria: {nueva_config.nota_aprobatoria}')
        self.stdout.write(f'  - Semestre límite electivas: {nueva_config.semestre_limite_electivas}')
        self.stdout.write(f'  - Total créditos obligatorios: {nueva_config.total_creditos_obligatorios}')

