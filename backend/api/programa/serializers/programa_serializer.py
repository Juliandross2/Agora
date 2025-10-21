from rest_framework import serializers
from api.programa.models.programa import Programa

class ProgramaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Programa"""
    
    class Meta:
        model = Programa
        fields = ['programa_id', 'nombre_programa', 'es_activo']
        read_only_fields = ['programa_id']
    
    def validate_nombre_programa(self, value):
        """Validar nombre del programa"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del programa no puede estar vacío")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre del programa debe tener al menos 3 caracteres")
        
        if len(value.strip()) > 100:
            raise serializers.ValidationError("El nombre del programa no puede exceder 100 caracteres")
        
        return value.strip()
    
    def validate_es_activo(self, value):
        """Validar estado activo"""
        if not isinstance(value, bool):
            raise serializers.ValidationError("El campo es_activo debe ser verdadero o falso")
        return value

class ProgramaCreateSerializer(serializers.Serializer):
    """Serializer para crear programa"""
    nombre_programa = serializers.CharField(max_length=100, required=True)
    es_activo = serializers.BooleanField(default=True, required=False)
    
    def validate_nombre_programa(self, value):
        """Validar nombre del programa"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del programa no puede estar vacío")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre del programa debe tener al menos 3 caracteres")
        
        if len(value.strip()) > 100:
            raise serializers.ValidationError("El nombre del programa no puede exceder 100 caracteres")
        
        # Verificar que no exista un programa con el mismo nombre
        if Programa.objects.filter(nombre_programa__iexact=value.strip()).exists():
            raise serializers.ValidationError("Ya existe un programa con este nombre")
        
        return value.strip()

class ProgramaUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar programa"""
    nombre_programa = serializers.CharField(max_length=100, required=False)
    es_activo = serializers.BooleanField(required=False)
    
    def validate_nombre_programa(self, value):
        """Validar nombre del programa"""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError("El nombre del programa no puede estar vacío")
            
            if len(value.strip()) < 3:
                raise serializers.ValidationError("El nombre del programa debe tener al menos 3 caracteres")
            
            if len(value.strip()) > 100:
                raise serializers.ValidationError("El nombre del programa no puede exceder 100 caracteres")
            
            return value.strip()
        return value
