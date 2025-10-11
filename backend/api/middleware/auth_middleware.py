from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from api.usuario.services.usuario_service import UsuarioService
import jwt
from django.conf import settings

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware personalizado para manejar autenticación JWT con modelo Usuario personalizado
    """
    
    # URLs que no requieren autenticación
    EXEMPT_URLS = [
        '/admin/',
        '/api/usuario/login/',
        '/api/usuario/register/',
        '/api/usuario/test/',
        '/api/auth/token/refresh/',
    ]
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.usuario_service = UsuarioService()
    
    def process_request(self, request):
        """
        Procesa la request antes de que llegue a la vista
        """
        path = request.path
        
        # Verificar si la URL está exenta de autenticación
        if any(path.startswith(exempt_url) for exempt_url in self.EXEMPT_URLS):
            return None
            
        # Verificar si es una request OPTIONS (preflight CORS)
        if request.method == 'OPTIONS':
            return None
        
        # Extraer token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({
                'error': 'Token de autenticación requerido',
                'code': 'AUTHENTICATION_REQUIRED'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decodificar token para obtener información del usuario
            decoded_token = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            
            user_id = decoded_token.get('user_id')
            if not user_id:
                return JsonResponse({
                    'error': 'Token inválido: user_id no encontrado',
                    'code': 'INVALID_TOKEN'
                }, status=401)
            
            # Obtener usuario de la base de datos
            usuario = self.usuario_service.obtener_usuario_por_id(user_id)
            if not usuario:
                return JsonResponse({
                    'error': 'Usuario no encontrado',
                    'code': 'USER_NOT_FOUND'
                }, status=401)
            
            # Agregar información del usuario al request
            request.user_id = user_id
            request.usuario = usuario
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'error': 'Token expirado',
                'code': 'TOKEN_EXPIRED'
            }, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({
                'error': 'Token inválido',
                'code': 'INVALID_TOKEN'
            }, status=401)
        except Exception as e:
            return JsonResponse({
                'error': f'Error de autenticación: {str(e)}',
                'code': 'AUTHENTICATION_ERROR'
            }, status=500)
            
        return None