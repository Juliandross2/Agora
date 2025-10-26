from api.oferta_electiva.repositories.repository_oferta_electiva import OfertaElectivaRepository
from api.oferta_electiva.serializers.serializer_oferta_electiva import (
	OfertaElectivaCreateUpdateSerializer,
	OfertaElectivaResponseSerializer
)

class OfertaElectivaService:
	def __init__(self):
		self.repo = OfertaElectivaRepository()

	def crear_oferta(self, data: dict):
		# validar campos básicos con serializer
		serializer = OfertaElectivaCreateUpdateSerializer(data=data)
		if not serializer.is_valid():
			return False, {'error': 'Datos inválidos', 'details': serializer.errors}

		created = self.repo.create(serializer.validated_data)
		resp = OfertaElectivaResponseSerializer(created).data
		return True, resp

	def listar_ofertas_activas(self):
		objs = self.repo.list_active()
		resp = OfertaElectivaResponseSerializer(objs, many=True).data
		return True, resp

	def obtener_oferta_activa(self, pk: int):
		obj = self.repo.get_active_by_id(pk)
		if not obj:
			return False, {'error': 'Oferta no encontrada o inactiva'}
		return True, OfertaElectivaResponseSerializer(obj).data

	def actualizar_oferta(self, pk: int, data: dict):
		obj = self.repo.get_active_by_id(pk)
		if not obj:
			return False, {'error': 'Oferta no encontrada o inactiva'}
		serializer = OfertaElectivaCreateUpdateSerializer(data=data, partial=True)
		if not serializer.is_valid():
			return False, {'error': 'Datos inválidos', 'details': serializer.errors}
		updated = self.repo.update(obj, serializer.validated_data)
		return True, OfertaElectivaResponseSerializer(updated).data

	def eliminar_oferta(self, pk: int):
		# soft delete: solo si está activa
		obj = self.repo.get_active_by_id(pk)
		if not obj:
			return False, {'error': 'Oferta no encontrada o ya inactiva'}
		self.repo.soft_delete(obj)
		return True, {'message': 'Oferta marcada como inactiva'}
