from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from api.usuario.serializers.usuario_serializer import (
    UsuarioRegisterSerializer, 
    UsuarioResponseSerializer
)
from api.usuario.models.usuario import Usuario
from typing import Dict, Tuple, Optional

class UsuarioService:
    """Servicio para manejar la lógica de negocio del Usuario"""
    
    def registrar_usuario(self, data: dict) -> Tuple[bool, Dict]:
        """
        Registrar un nuevo usuario
        Returns: (success: bool, response: dict)
        """
        try:
            # Validar datos con serializer
            serializer = UsuarioRegisterSerializer(data=data)
            if not serializer.is_valid():
                return False, {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }
            
            # Verificar si el email ya existe
            if Usuario.objects.filter(email_usuario=data['email_usuario']).exists():
                return False, {
                    'error': 'El email ya está registrado'
                }
            
            # Verificar si el nombre de usuario ya existe
            if Usuario.objects.filter(nombre_usuario=data['nombre_usuario']).exists():
                return False, {
                    'error': 'El nombre de usuario ya existe'
                }
            
            # Crear usuario
            usuario = serializer.save()
            
            # Generar tokens JWT
            refresh = RefreshToken()
            refresh['user_id'] = usuario.usuario_id
            refresh['email'] = usuario.email_usuario
            
            # Serializar usuario para respuesta
            usuario_serializer = UsuarioResponseSerializer(usuario)
            
            return True, {
                'message': 'Usuario registrado exitosamente',
                'user': usuario_serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            
        except Exception as e:
            return False, {
                'error': 'Error interno del servidor',
                'details': str(e)
            }
    
    def autenticar_usuario(self, email: str, contrasenia: str) -> Tuple[bool, Dict]:
        """
        Autenticar usuario con email y contraseña
        Returns: (success: bool, response: dict)
        """
        try:
            from django.contrib.auth.hashers import check_password
            
            # Buscar usuario por email
            try:
                usuario = Usuario.objects.get(email_usuario=email, es_activo=True)
            except Usuario.DoesNotExist:
                return False, {
                    'error': 'Usuario no encontrado'
                }
            
            # Verificar contraseña
            if not check_password(contrasenia, usuario.contrasenia):
                return False, {
                    'error': 'Contraseña incorrecta'
                }
            
            # Generar tokens JWT
            refresh = RefreshToken()
            refresh['user_id'] = usuario.usuario_id
            refresh['email'] = usuario.email_usuario
            
            # Serializar usuario para respuesta
            usuario_serializer = UsuarioResponseSerializer(usuario)
            
            return True, {
                'message': 'Login exitoso',
                'user': usuario_serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            
        except Exception as e:
            return False, {
                'error': 'Error interno del servidor',
                'details': str(e)
            }
    
    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        try:
            return Usuario.objects.get(usuario_id=usuario_id, es_activo=True)
        except Usuario.DoesNotExist:
            return None
    
    def obtener_perfil_usuario(self, usuario_id: int) -> Tuple[bool, Dict]:
        """
        Obtener perfil de usuario
        Returns: (success: bool, response: dict)
        """
        try:
            usuario = self.obtener_usuario_por_id(usuario_id)
            
            if not usuario:
                return False, {
                    'error': 'Usuario no encontrado'
                }
            
            usuario_serializer = UsuarioResponseSerializer(usuario)
            
            return True, {
                'user': usuario_serializer.data
            }
            
        except Exception as e:
            return False, {
                'error': 'Error interno del servidor',
                'details': str(e)
            }

    def desactivar_usuario(self, usuario_id: int) -> Tuple[bool, Dict]:
        """
        Desactiva el usuario indicado.
        Restricciones:
         - No permite desactivar el último usuario activo del sistema.
         - El controller debe verificar que el token pertenezca al mismo usuario que se intenta desactivar.
        Returns: (success: bool, response: dict)
        """
        try:
            usuario = self.obtener_usuario_por_id(usuario_id)
            if not usuario:
                return False, {'error': 'Usuario no encontrado'}

            # Contar usuarios activos
            activos_count = Usuario.objects.filter(es_activo=True).count()
            if activos_count <= 1:
                return False, {
                    'error': 'No se puede desactivar el último usuario activo. Designe otro usuario activo antes de desactivar esta cuenta.'
                }

            # Desactivación lógica
            usuario.es_activo = False
            usuario.save()

            usuario_serializer = UsuarioResponseSerializer(usuario)
            return True, {
                'message': 'Usuario desactivado correctamente',
                'user': usuario_serializer.data
            }

        except Exception as e:
            return False, {
                'error': 'Error interno del servidor',
                'details': str(e)
            }