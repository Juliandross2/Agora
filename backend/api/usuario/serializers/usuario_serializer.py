from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from api.usuario.models.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    contrasenia = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Usuario
        fields = ['usuario_id', 'nombre_usuario', 'email_usuario', 'contrasenia', 'es_activo', 'es_admin']
        extra_kwargs = {
            'contrasenia': {'write_only': True},
            'usuario_id': {'read_only': True},
            'es_admin': {'read_only': True}
        }

    def validate_contrasenia(self, value):
        """Validar la contraseña"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        """Crear usuario con contraseña hasheada"""
        validated_data['contrasenia'] = make_password(validated_data['contrasenia'])
        return super().create(validated_data)

class UsuarioLoginSerializer(serializers.Serializer):
    """Serializer para login de usuario"""
    email_usuario = serializers.EmailField()
    contrasenia = serializers.CharField(write_only=True)

class UsuarioRegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuario"""
    contrasenia = serializers.CharField(write_only=True, min_length=8)
    confirmar_contrasenia = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'email_usuario', 'contrasenia', 'confirmar_contrasenia']

    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        if attrs['contrasenia'] != attrs['confirmar_contrasenia']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs

    def validate_contrasenia(self, value):
        """Validar la contraseña"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        """Crear usuario"""
        validated_data.pop('confirmar_contrasenia')
        validated_data['contrasenia'] = make_password(validated_data['contrasenia'])
        return Usuario.objects.create(**validated_data)

class UsuarioResponseSerializer(serializers.ModelSerializer):
    """Serializer para respuesta de usuario (sin contraseña)"""
    class Meta:
        model = Usuario
        fields = ['usuario_id', 'nombre_usuario', 'email_usuario', 'es_activo', 'es_admin']