from api.pensum.repositories.repository_pensum import PensumRepository
from api.pensum.serializers.serializer_pensum import PensumSerializer
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
        return True, PensumSerializer(obj).data

    def crear_pensum(self, data):
        # data expected validated by serializer in controller, but validate again defensively
        try:
            programa_id = int(data.get('programa_id'))
            programa = Programa.objects.get(pk=programa_id)
        except (TypeError, ValueError, Programa.DoesNotExist):
            return False, {'error': 'Programa inválido o no encontrado'}

        anio = data.get('anio_creacion', None)
        es_activo = data.get('es_activo', True)

        pensum = self.repo.create(programa, anio_creacion=anio, es_activo=es_activo)
        return True, PensumSerializer(pensum).data

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
        return True, PensumSerializer(pensum).data

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