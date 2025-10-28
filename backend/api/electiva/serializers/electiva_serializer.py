from rest_framework import serializers
from api.electiva.models.electiva import Electiva

class ElectivaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Electiva"""
    
    class Meta:
        model = Electiva
        fields = ['electiva_id', 'programa_id', 'nombre_electiva', 'es_activa']
        read_only_fields = ['electiva_id']
    
    def validate_nombre_electiva(self, value):
        """Validar nombre de la electiva"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la electiva no puede estar vacío")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre de la electiva debe tener al menos 3 caracteres")
        
        if len(value.strip()) > 100:
            raise serializers.ValidationError("El nombre de la electiva no puede exceder 100 caracteres")
        
        return value.strip()

class ElectivaCreateSerializer(serializers.Serializer):
    """Serializer para crear electiva"""
    programa_id = serializers.IntegerField(required=True)
    nombre_electiva = serializers.CharField(max_length=100, required=True)
    es_activa = serializers.BooleanField(default=True, required=False)
    
    def validate_nombre_electiva(self, value):
        """Validar nombre de la electiva"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la electiva no puede estar vacío")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre de la electiva debe tener al menos 3 caracteres")
        
        if len(value.strip()) > 100:
            raise serializers.ValidationError("El nombre de la electiva no puede exceder 100 caracteres")
        
        return value.strip()
    
    def validate_programa_id(self, value):
        """Validar que el programa_id existe"""
        from api.programa.models.programa import Programa
        
        if value <= 0:
            raise serializers.ValidationError("El ID del programa debe ser mayor a 0")
        
        try:
            Programa.objects.get(programa_id=value)
        except Programa.DoesNotExist:
            raise serializers.ValidationError("El programa especificado no existe")
        
        return value

class ElectivaUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar electiva"""
    programa_id = serializers.IntegerField(required=False)
    nombre_electiva = serializers.CharField(max_length=100, required=False)
    es_activa = serializers.BooleanField(required=False)
    
    def validate_nombre_electiva(self, value):
        """Validar nombre de la electiva"""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError("El nombre de la electiva no puede estar vacío")
            
            if len(value.strip()) < 3:
                raise serializers.ValidationError("El nombre de la electiva debe tener al menos 3 caracteres")
            
            if len(value.strip()) > 100:
                raise serializers.ValidationError("El nombre de la electiva no puede exceder 100 caracteres")
            
            return value.strip()
        return value
    
    def validate_programa_id(self, value):
        """Validar que el programa_id existe"""
        if value is not None:
            from api.programa.models.programa import Programa
            
            if value <= 0:
                raise serializers.ValidationError("El ID del programa debe ser mayor a 0")
            
            try:
                Programa.objects.get(programa_id=value)
            except Programa.DoesNotExist:
                raise serializers.ValidationError("El programa especificado no existe")
        
        return value

