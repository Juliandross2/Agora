from api.pensum.repositories.repository_pensum import PensumRepository
from api.pensum.serializers.serializer_pensum import PensumSerializer, PensumDetailSerializer
from api.programa.models.programa import Programa
from django.core.exceptions import ObjectDoesNotExist

class PensumService:
    def __init__(self):
        self.repo = PensumRepository()

    def obtener_todos_pensums(self):
        objs = self.repo.get_all()
        data = PensumSerializer(objs, many=True).data
        return True, data

    def obtener_pensum_por_id(self, pensum_id):
        obj = self.repo.get_by_id(pensum_id)
        if not obj:
            return False, {'error': 'Pensum no encontrado'}
        return True, PensumDetailSerializer(obj).data

    def obtener_estadisticas_pensum(self, pensum_id):
        """Obtiene estadísticas detalladas del pensum"""
        obj = self.repo.get_by_id(pensum_id)
        if not obj:
            return False, {'error': 'Pensum no encontrado'}
        
        estadisticas = {
            'pensum_id': obj.pensum_id,
            'programa_nombre': obj.programa_id.nombre_programa if obj.programa_id else 'N/A',
            'anio_creacion': obj.anio_creacion,
            'creditos_obligatorios_totales': obj.creditos_obligatorios_totales,
            'total_materias_obligatorias': obj.total_materias_obligatorias,
            'total_materias_electivas': obj.total_materias_electivas,
            'total_materias': obj.total_materias_obligatorias + obj.total_materias_electivas,
            'es_activo': obj.es_activo
        }
        return True, estadisticas

    def crear_pensum(self, data):
        try:
            programa_id = int(data.get('programa_id'))
            programa = Programa.objects.get(pk=programa_id)
        except (TypeError, ValueError, Programa.DoesNotExist):
            return False, {'error': 'Programa inválido o no encontrado'}

        anio = data.get('anio_creacion', None)
        es_activo = data.get('es_activo', True)

        pensum = self.repo.create(programa, anio_creacion=anio, es_activo=es_activo)
        return True, PensumDetailSerializer(pensum).data

    def actualizar_pensum(self, pensum_id, data):
        pensum = self.repo.get_by_id(pensum_id)
        if not pensum:
            return False, {'error': 'Pensum no encontrado'}

        update_fields = {}
        if 'programa_id' in data:
            try:
                programa = Programa.objects.get(pk=int(data['programa_id']))
                update_fields['programa_id'] = programa
            except (TypeError, ValueError, Programa.DoesNotExist):
                return False, {'error': 'Programa inválido o no encontrado'}
        if 'anio_creacion' in data:
            update_fields['anio_creacion'] = data.get('anio_creacion')
        if 'es_activo' in data:
            update_fields['es_activo'] = data.get('es_activo')

        pensum = self.repo.update(pensum, **update_fields)
        return True, PensumDetailSerializer(pensum).data

    def eliminar_pensum(self, pensum_id):
        pensum = self.repo.get_by_id(pensum_id)
        if not pensum:
            return False, {'error': 'Pensum no encontrado'}
        self.repo.delete(pensum)
        return True, {'message': 'Pensum eliminado correctamente'}

    def obtener_pensums_activos(self):
        objs = self.repo.get_active()
        data = PensumSerializer(objs, many=True).data
        return True, data

    def buscar_pensums_por_programa(self, programa_id):
        try:
            int(programa_id)
        except (TypeError, ValueError):
            return False, {'error': 'programa_id inválido'}
        objs = self.repo.filter_by_programa(programa_id)
        data = PensumSerializer(objs, many=True).data
        return True, data

    def obtener_resumen_creditos_por_programa(self, programa_id):
        """Obtiene un resumen de créditos de todos los pensums de un programa"""
        try:
            int(programa_id)
        except (TypeError, ValueError):
            return False, {'error': 'programa_id inválido'}
            
        pensums = self.repo.filter_by_programa(programa_id)
        resumen = []
        
        for pensum in pensums:
            resumen.append({
                'pensum_id': pensum.pensum_id,
                'anio_creacion': pensum.anio_creacion,
                'creditos_obligatorios': pensum.creditos_obligatorios_totales,
                'materias_obligatorias': pensum.total_materias_obligatorias,
                'materias_electivas': pensum.total_materias_electivas,
                'es_activo': pensum.es_activo
            })
        
        return True, resumen