from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.usuario.services.usuario_service import UsuarioService
from api.usuario.serializers.usuario_serializer import UsuarioLoginSerializer, UsuarioRegisterSerializer, UsuarioResponseSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
import json

class UsuarioController:
    """Controller para manejar las peticiones HTTP relacionadas con Usuario"""
    
    def __init__(self):
        self.service = UsuarioService()

# Instancia global del controller
usuario_controller = UsuarioController()
@extend_schema(
    request=UsuarioRegisterSerializer,
    responses={
        201: OpenApiResponse(response=UsuarioResponseSerializer, description="Usuario creado"),
        400: OpenApiResponse(description="Campos inválidos")
    },
    examples=[
        OpenApiExample(
            "RegisterExample",
            value={
                "nombre_usuario": "john_doe",
                "email_usuario": "john.doe@example.com",
                "contrasenia": "MiPassword123!",
                "confirmar_contrasenia": "MiPassword123!"
            },
            media_type="application/json"
        )
    ],
)
@api_view(['POST'])
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

@extend_schema(
    request=UsuarioLoginSerializer,
    responses={
        200: OpenApiResponse(description="Login exitoso (devuelve tokens y datos de usuario)"),
        401: OpenApiResponse(description="Credenciales inválidas")
    },
    examples=[
        OpenApiExample(
            "LoginExample",
            value={
                "email_usuario": "john.doe@example.com",
                "contrasenia": "MiPassword123!"
            },
            media_type="application/json"
        ),
        OpenApiExample(
            "LoginResponseExample",
            value={
                "message": "Login exitoso",
                "user": {
                    "usuario_id": 1,
                    "nombre_usuario": "john_doe",
                    "email_usuario": "john.doe@example.com",
                    "es_activo": True
                },
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
            },
            media_type="application/json"
        )
    ]
)
@api_view(['POST'])
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
@extend_schema(
    responses={
        200: OpenApiResponse(response=UsuarioResponseSerializer, description="Perfil del usuario"),
        401: OpenApiResponse(description="Token inválido o no proporcionado")
    },
)
@api_view(['GET'])
def profile(request):
    """
    Obtener perfil del usuario autenticado
    """
    try:
        print(f"[CONTROLLER] Procesando perfil de usuario")
        print(f"[CONTROLLER] Headers: {dict(request.headers)}")
        
        # El usuario_id debe venir del middleware JWT
        user_id = getattr(request, 'user_id', None)
        usuario = getattr(request, 'usuario', None)
        
        print(f"[CONTROLLER] user_id del middleware: {user_id}")
        print(f"[CONTROLLER] usuario del middleware: {usuario}")
        
        if not user_id:
            print(f"[CONTROLLER] user_id no encontrado en el request")
            return Response({
                'error': 'Token inválido o usuario no encontrado',
                'debug': 'user_id no está en el request'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not usuario:
            print(f"[CONTROLLER] usuario no encontrado en el request")
            return Response({
                'error': 'Usuario no encontrado en el middleware',
                'debug': f'user_id encontrado: {user_id}'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Llamar al servicio para obtener perfil
        success, response = usuario_controller.service.obtener_perfil_usuario(user_id)
        
        if success:
            print(f"[CONTROLLER] Perfil obtenido exitosamente")
            return Response(response, status=status.HTTP_200_OK)
        else:
            print(f"[CONTROLLER] Error al obtener perfil")
            return Response({
                **response,
                'debug': f'Servicio falló para user_id: {user_id}'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        print(f"[CONTROLLER] Excepción en profile: {e}")
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e),
            'debug': f'Exception en profile endpoint'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@extend_schema(
    responses={200: OpenApiResponse(description="API Usuario funcionando correctamente")}
)
@api_view(['GET'])
def test_connection(request):
    """
    Endpoint de prueba para verificar conexión
    """
    return Response({
        'message': 'API Usuario funcionando correctamente',
        'status': 'OK'
    }, status=status.HTTP_200_OK)