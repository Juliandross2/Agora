from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from api.usuario.serializers.usuario_serializer import (
    UsuarioRegisterSerializer, 
    UsuarioResponseSerializer
)
from api.usuario.models.usuario import Usuario
from typing import Dict, Tuple, Optional
import re

class UsuarioService:
    """Servicio para manejar la lógica de negocio del Usuario"""
    
    def registrar_usuario(self, data: dict) -> Tuple[bool, Dict]:
        """
        Registrar un nuevo usuario
        Returns: (success: bool, response: dict)
        Mensajes de error mejorados y estructurados en:
         - error: mensaje general
         - details: errores por campo (si aplica)
        """
        try:
            # Validar datos con serializer
            serializer = UsuarioRegisterSerializer(data=data)
            if not serializer.is_valid():
                # Normalizar mensajes del serializer
                field_errors = {}
                for field, errors in serializer.errors.items():
                    # convertir lista de errores a texto
                    field_errors[field] = " ".join([str(e) for e in errors])
                return False, {
                    'error': 'Datos inválidos',
                    'details': field_errors
                }
            
            # Validaciones adicionales claras
            nombre = serializer.validated_data.get('nombre_usuario')
            email = serializer.validated_data.get('email_usuario')
            contrasenia = serializer.validated_data.get('contrasenia')
            confirmar = serializer.validated_data.get('confirmar_contrasenia')

            # confirmar contraseñas
            if contrasenia != confirmar:
                return False, {
                    'error': 'Contraseñas no coinciden',
                    'details': {'confirmar_contrasenia': 'La contraseña y su confirmación deben ser iguales.'}
                }

            # reglas mínimas de contraseña
            if len(contrasenia) < 8:
                return False, {
                    'error': 'Contraseña demasiado corta',
                    'details': {'contrasenia': 'La contraseña debe tener al menos 8 caracteres.'}
                }
            if not re.search(r'\d', contrasenia) or not re.search(r'[A-Za-z]', contrasenia):
                return False, {
                    'error': 'Contraseña débil',
                    'details': {'contrasenia': 'La contraseña debe contener letras y números.'}
                }

            # unicidad
            if Usuario.objects.filter(email_usuario=email).exists():
                return False, {
                    'error': 'Email ya registrado',
                    'details': {'email_usuario': 'Ya existe una cuenta con este correo.'}
                }
            if Usuario.objects.filter(nombre_usuario=nombre).exists():
                return False, {
                    'error': 'Nombre de usuario ya existe',
                    'details': {'nombre_usuario': 'El nombre de usuario ya está en uso.'}
                }
            
            # Crear usuario vía serializer (asume que el serializer maneja el hashing)
            usuario = serializer.save()
            
            # Generar tokens JWT (ejemplo; el middleware/uso puede requerir RefreshToken.for_user)
            refresh = RefreshToken()
            refresh['user_id'] = usuario.usuario_id
            refresh['email'] = usuario.email_usuario
            
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

    def listar_usuarios(self, activos: Optional[bool] = None) -> Tuple[bool, Dict]:
        """
        Listar usuarios.
        activos = None -> todos
        activos = True -> solo activos
        activos = False -> solo inactivos
        """
        try:
            if activos is None:
                qs = Usuario.objects.all()
            elif activos:
                qs = Usuario.objects.filter(es_activo=True)
            else:
                qs = Usuario.objects.filter(es_activo=False)

            serializer = UsuarioResponseSerializer(qs, many=True)
            return True, serializer.data

        except Exception as e:
            return False, {'error': 'Error interno del servidor', 'details': str(e)}

    def listar_usuarios_activos(self) -> Tuple[bool, Dict]:
        return self.listar_usuarios(activos=True)

    def listar_usuarios_inactivos(self) -> Tuple[bool, Dict]:
        return self.listar_usuarios(activos=False)

    def activar_usuario(self, usuario_id: int) -> Tuple[bool, Dict]:
        """
        Activa un usuario desactivado.
        - Busca el usuario (incluyendo inactivos).
        - Si ya está activo devuelve error.
        - Retorna usuario serializado al activarlo.
        """
        try:
            try:
                usuario = Usuario.objects.get(usuario_id=usuario_id)
            except Usuario.DoesNotExist:
                return False, {'error': 'Usuario no encontrado'}

            if usuario.es_activo:
                return False, {'error': 'Usuario ya está activo'}

            usuario.es_activo = True
            usuario.save()

            usuario_serializer = UsuarioResponseSerializer(usuario)
            return True, {
                'message': 'Usuario activado correctamente',
                'user': usuario_serializer.data
            }

        except Exception as e:
            return False, {
                'error': 'Error interno del servidor',
                'details': str(e)
            }