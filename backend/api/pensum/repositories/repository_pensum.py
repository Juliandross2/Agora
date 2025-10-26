from api.pensum.models.pensum import Pensum
from api.programa.models.programa import Programa
from django.core.exceptions import ObjectDoesNotExist

class PensumRepository:
    def get_all(self):
        return Pensum.objects.all()

    def get_by_id(self, pensum_id):
        try:
            return Pensum.objects.get(pk=pensum_id)
        except ObjectDoesNotExist:
            return None

    def create(self, programa_obj, anio_creacion=None, es_activo=True):
        pensum = Pensum.objects.create(
            programa_id=programa_obj,
            anio_creacion=anio_creacion,
            es_activo=es_activo
        )
        return pensum

    def update(self, pensum_obj, **fields):
        for key, value in fields.items():
            setattr(pensum_obj, key, value)
        pensum_obj.save()
        return pensum_obj
    #Desactivación lógica
    def delete(self, pensum_obj):
        pensum_obj.es_activo = False
        pensum_obj.save()
        return True

    def get_active(self):
        return Pensum.objects.filter(es_activo=True)

    def filter_by_programa(self, programa_id):
        return Pensum.objects.filter(programa_id__pk=programa_id)