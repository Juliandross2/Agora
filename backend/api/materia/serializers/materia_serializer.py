from rest_framework import serializers
from api.materia.models.materia import Materia

class MateriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Materia"""
    
    class Meta:
        model = Materia
        fields = ['materia_id', 'pensum_id', 'nombre_materia', 'creditos', 'es_obligatoria', 'es_activa', 'semestre']
        read_only_fields = ['materia_id']
    
    def validate_nombre_materia(self, value):
        """Validar nombre de la materia"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la materia no puede estar vacío")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre de la materia debe tener al menos 3 caracteres")
        
        if len(value.strip()) > 100:
            raise serializers.ValidationError("El nombre de la materia no puede exceder 100 caracteres")
        
        return value.strip()
    
    def validate_creditos(self, value):
        """Validar créditos"""
        if value is None:
            raise serializers.ValidationError("Los créditos son obligatorios")
        
        if value <= 0:
            raise serializers.ValidationError("Los créditos deben ser mayores a 0")
        
        if value > 10:
            raise serializers.ValidationError("Los créditos no pueden ser mayores a 10")
        
        return value
    
    def validate_semestre(self, value):
        """Validar semestre"""
        if value is None:
            raise serializers.ValidationError("El semestre es obligatorio")
        
        if value <= 0:
            raise serializers.ValidationError("El semestre debe ser mayor a 0")
        
        if value > 12:
            raise serializers.ValidationError("El semestre no puede ser mayor a 12")
        
        return value

class MateriaCreateSerializer(serializers.Serializer):
    """Serializer para crear materia"""
    pensum_id = serializers.IntegerField(required=True)
    nombre_materia = serializers.CharField(max_length=100, required=True)
    creditos = serializers.IntegerField(required=True)
    es_obligatoria = serializers.BooleanField(default=True, required=False)
    es_activa = serializers.BooleanField(default=True, required=False)
    semestre = serializers.IntegerField(required=True)
    
    def validate_nombre_materia(self, value):
        """Validar nombre de la materia"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la materia no puede estar vacío")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre de la materia debe tener al menos 3 caracteres")
        
        if len(value.strip()) > 100:
            raise serializers.ValidationError("El nombre de la materia no puede exceder 100 caracteres")
        
        return value.strip()
    
    def validate_creditos(self, value):
        """Validar créditos"""
        if value <= 0:
            raise serializers.ValidationError("Los créditos deben ser mayores a 0")
        
        if value > 10:
            raise serializers.ValidationError("Los créditos no pueden ser mayores a 10")
        
        return value
    
    def validate_semestre(self, value):
        """Validar semestre"""
        if value <= 0:
            raise serializers.ValidationError("El semestre debe ser mayor a 0")
        
        if value > 12:
            raise serializers.ValidationError("El semestre no puede ser mayor a 12")
        
        return value
    
    def validate_pensum_id(self, value):
        """Validar que el pensum_id existe"""
        from api.pensum.models.pensum import Pensum
        
        if value <= 0:
            raise serializers.ValidationError("El ID del pensum debe ser mayor a 0")
        
        try:
            Pensum.objects.get(pensum_id=value)
        except Pensum.DoesNotExist:
            raise serializers.ValidationError("El pensum especificado no existe")
        
        return value

class MateriaUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar materia"""
    pensum_id = serializers.IntegerField(required=False)
    nombre_materia = serializers.CharField(max_length=100, required=False)
    creditos = serializers.IntegerField(required=False)
    es_obligatoria = serializers.BooleanField(required=False)
    es_activa = serializers.BooleanField(required=False)
    semestre = serializers.IntegerField(required=False)
    
    def validate_nombre_materia(self, value):
        """Validar nombre de la materia"""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError("El nombre de la materia no puede estar vacío")
            
            if len(value.strip()) < 3:
                raise serializers.ValidationError("El nombre de la materia debe tener al menos 3 caracteres")
            
            if len(value.strip()) > 100:
                raise serializers.ValidationError("El nombre de la materia no puede exceder 100 caracteres")
            
            return value.strip()
        return value
    
    def validate_creditos(self, value):
        """Validar créditos"""
        if value is not None:
            if value <= 0:
                raise serializers.ValidationError("Los créditos deben ser mayores a 0")
            
            if value > 10:
                raise serializers.ValidationError("Los créditos no pueden ser mayores a 10")
        
        return value
    
    def validate_semestre(self, value):
        """Validar semestre"""
        if value is not None:
            if value <= 0:
                raise serializers.ValidationError("El semestre debe ser mayor a 0")
            
            if value > 12:
                raise serializers.ValidationError("El semestre no puede ser mayor a 12")
        
        return value
    
    def validate_pensum_id(self, value):
        """Validar que el pensum_id existe"""
        if value is not None:
            from api.pensum.models.pensum import Pensum
            
            if value <= 0:
                raise serializers.ValidationError("El ID del pensum debe ser mayor a 0")
            
            try:
                Pensum.objects.get(pensum_id=value)
            except Pensum.DoesNotExist:
                raise serializers.ValidationError("El pensum especificado no existe")
        
        return value

