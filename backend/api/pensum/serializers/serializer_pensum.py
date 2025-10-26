from rest_framework import serializers
from api.pensum.models.pensum import Pensum
from api.programa.models.programa import Programa

class PensumSerializer(serializers.ModelSerializer):
    programa_id = serializers.PrimaryKeyRelatedField(read_only=True, source='programa_id')

    class Meta:
        model = Pensum
        fields = ['pensum_id', 'programa_id', 'anio_creacion', 'es_activo']

class PensumCreateUpdateSerializer(serializers.Serializer):
    programa_id = serializers.IntegerField()
    anio_creacion = serializers.IntegerField(required=False, allow_null=True)
    es_activo = serializers.BooleanField(required=False, default=True)

    def validate_programa_id(self, value):
        try:
            Programa.objects.get(pk=value)
        except Programa.DoesNotExist:
            raise serializers.ValidationError("Programa no encontrado")
        return value