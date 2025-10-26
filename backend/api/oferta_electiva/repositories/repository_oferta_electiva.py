from api.oferta_electiva.models.oferta_electiva import OfertaElectiva

class OfertaElectivaRepository:
	"""Repositorio para acceso directo al modelo OfertaElectiva"""

	def create(self, data: dict) -> OfertaElectiva:
		# Django permite pasar electiva_id como kwarg
		return OfertaElectiva.objects.create(
			electiva_id=data.get('electiva_id'),
			periodo=data.get('periodo'),
			es_activa=data.get('es_activa', True)
		)

	def list_active(self):
		return OfertaElectiva.objects.filter(es_activa=True).order_by('-oferta_electiva_id')

	def get_active_by_id(self, pk: int):
		try:
			return OfertaElectiva.objects.get(pk=pk, es_activa=True)
		except OfertaElectiva.DoesNotExist:
			return None

	def update(self, obj: OfertaElectiva, data: dict) -> OfertaElectiva:
		# solo actualizamos campos permitidos
		if 'electiva_id' in data:
			obj.electiva_id = data['electiva_id']
		if 'periodo' in data:
			obj.periodo = data['periodo']
		# es_activa no se permite activar desde update arbitrariamente; lo respetamos si viene explícito
		if 'es_activa' in data:
			obj.es_activa = data['es_activa']
		obj.save()
		return obj

	def soft_delete(self, obj: OfertaElectiva) -> OfertaElectiva:
		obj.es_activa = False
		obj.save()
		return obj
