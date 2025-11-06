from api.pensum.models.pensum import Pensum
from api.programa.models.programa import Programa
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

class PensumRepository:
    def get_all(self):
        return Pensum.objects.all()

    def get_by_id(self, pensum_id):
        try:
            return Pensum.objects.get(pk=pensum_id)
        except ObjectDoesNotExist:
            return None

    def get_by_programa(self, programa_id):
        """Obtener pensums por programa"""
        return Pensum.objects.filter(programa_id__pk=programa_id).order_by('-anio_creacion')

    def get_active_by_programa(self, programa_id):
        """Obtener pensums activos por programa"""
        return Pensum.objects.filter(programa_id__pk=programa_id, es_activo=True).order_by('-anio_creacion')

    def get_current_by_programa(self, programa_id):
        """Obtener el pensum actual (activo) de un programa"""
        try:
            return Pensum.objects.filter(programa_id__pk=programa_id, es_activo=True).first()
        except ObjectDoesNotExist:
            return None

    @transaction.atomic
    def create(self, programa_obj, anio_creacion=None, es_activo=True):
        """Crear pensum, desactivando otros si es_activo=True"""
        if es_activo:
            # Desactivar todos los pensums activos del mismo programa
            Pensum.objects.filter(programa_id=programa_obj, es_activo=True).update(es_activo=False)
        
        pensum = Pensum.objects.create(
            programa_id=programa_obj,
            anio_creacion=anio_creacion,
            es_activo=es_activo
        )
        return pensum

    @transaction.atomic
    def update(self, pensum_obj, **fields):
        """Actualizar pensum, manejando la lógica de pensum único activo"""
        # Si se está activando este pensum
        if fields.get('es_activo') is True and not pensum_obj.es_activo:
            # Desactivar todos los otros pensums del mismo programa
            Pensum.objects.filter(
                programa_id=pensum_obj.programa_id, 
                es_activo=True
            ).exclude(pk=pensum_obj.pk).update(es_activo=False)
        
        for key, value in fields.items():
            setattr(pensum_obj, key, value)
        pensum_obj.save()
        return pensum_obj

    def delete(self, pensum_obj):
        """Desactivación lógica"""
        pensum_obj.es_activo = False
        pensum_obj.save()
        return True

    def get_active(self):
        """Obtener todos los pensums activos"""
        return Pensum.objects.filter(es_activo=True)

    def filter_by_programa(self, programa_id):
        """Filtrar pensums por programa"""
        return Pensum.objects.filter(programa_id__pk=programa_id).order_by('-anio_creacion')

    def validate_unique_active_per_programa(self, programa_id, exclude_pensum_id=None):
        """Validar que solo haya un pensum activo por programa"""
        query = Pensum.objects.filter(programa_id__pk=programa_id, es_activo=True)
        if exclude_pensum_id:
            query = query.exclude(pk=exclude_pensum_id)
        return query.exists()