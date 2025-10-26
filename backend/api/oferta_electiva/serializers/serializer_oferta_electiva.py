from rest_framework import serializers
from api.oferta_electiva.models.oferta_electiva import OfertaElectiva

class OfertaElectivaCreateUpdateSerializer(serializers.Serializer):
	# recibimos electiva_id como entero (Django acepta electiva_id al crear)
	electiva_id = serializers.IntegerField()
	periodo = serializers.IntegerField()
	# es_activa no debe ser requerido al crear (por defecto True)
	es_activa = serializers.BooleanField(required=False)

class OfertaElectivaResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = OfertaElectiva
		fields = ['oferta_electiva_id', 'electiva_id', 'periodo', 'es_activa']
