from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.usuario.services.usuario_service import UsuarioService
from api.usuario.serializers.usuario_serializer import UsuarioLoginSerializer
import json

class UsuarioController:
    """Controller para manejar las peticiones HTTP relacionadas con Usuario"""
    
    def __init__(self):
        self.service = UsuarioService()

# Instancia global del controller
usuario_controller = UsuarioController()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registrar un nuevo usuario
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Validar que se envíen los campos requeridos
        required_fields = ['nombre_usuario', 'email_usuario', 'contrasenia', 'confirmar_contrasenia']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return Response({
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Llamar al servicio para registrar usuario
        success, response = usuario_controller.service.registrar_usuario(data)
        
        if success:
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'JSON inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Autenticar usuario (login)
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Validar datos con serializer
        serializer = UsuarioLoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'error': 'Datos inválidos',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extraer email y contraseña
        email = serializer.validated_data['email_usuario']
        contrasenia = serializer.validated_data['contrasenia']
        
        # Llamar al servicio para autenticar usuario
        success, response = usuario_controller.service.autenticar_usuario(email, contrasenia)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'JSON inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Obtener perfil del usuario autenticado
    """
    try:
        # El usuario_id debe venir del token JWT decodificado
        # Para esto necesitamos modificar el middleware para extraer el user_id del token
        user_id = getattr(request, 'user_id', None)
        
        if not user_id:
            return Response({
                'error': 'Token inválido o usuario no encontrado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Llamar al servicio para obtener perfil
        success, response = usuario_controller.service.obtener_perfil_usuario(user_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def test_connection(request):
    """
    Endpoint de prueba para verificar conexión
    """
    return Response({
        'message': 'API Usuario funcionando correctamente',
        'status': 'OK'
    }, status=status.HTTP_200_OK)