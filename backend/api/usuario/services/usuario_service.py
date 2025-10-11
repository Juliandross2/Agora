from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from api.usuario.repositories.usuario_repository import UsuarioRepository
from api.usuario.serializers.usuario_serializer import (
    UsuarioRegisterSerializer, 
    UsuarioResponseSerializer
)
from api.usuario.models.usuario import Usuario
from typing import Dict, Tuple, Optional

class UsuarioService:
    """Servicio para manejar la lógica de negocio del Usuario"""
    
    def __init__(self):
        self.repository = UsuarioRepository()
    
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
            if self.repository.existe_email(data['email_usuario']):
                return False, {
                    'error': 'El email ya está registrado'
                }
            
            # Verificar si el nombre de usuario ya existe
            if self.repository.existe_nombre_usuario(data['nombre_usuario']):
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
            
        except ValidationError as e:
            return False, {
                'error': 'Error de validación',
                'details': str(e)
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
            # Buscar usuario por email
            usuario = self.repository.obtener_por_email(email)
            
            if not usuario:
                return False, {
                    'error': 'Usuario no encontrado'
                }
            
            # Verificar contraseña
            if not self.repository.verificar_contrasenia(usuario, contrasenia):
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
        return self.repository.obtener_por_id(usuario_id)
    
    def obtener_perfil_usuario(self, usuario_id: int) -> Tuple[bool, Dict]:
        """
        Obtener perfil de usuario
        Returns: (success: bool, response: dict)
        """
        try:
            usuario = self.repository.obtener_por_id(usuario_id)
            
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