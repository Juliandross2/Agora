from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
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
        '/api/docs/swagger/',
        '/api/schema/',
        '/api/docs/redoc/',
        '/api/historias/',  # Permitir acceso a endpoints de historias
    ]
    
    def process_request(self, request):
        """
        Procesa la request antes de que llegue a la vista
        """
        path = request.path
        print(f"[MIDDLEWARE] Procesando ruta: {path}")
        print(f"[MIDDLEWARE] Método: {request.method}")
        
        # Verificar si la URL está exenta de autenticación
        if any(path.startswith(exempt_url) for exempt_url in self.EXEMPT_URLS):
            print(f"[MIDDLEWARE] Ruta exenta de autenticación: {path}")
            return None
            
        # Verificar si es una request OPTIONS (preflight CORS)
        if request.method == 'OPTIONS':
            print(f"[MIDDLEWARE] Request OPTIONS detectada")
            return None
        
        # Extraer token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print(f"[MIDDLEWARE] Authorization header: {auth_header}")
        
        if not auth_header or not auth_header.startswith('Bearer '):
            print(f"[MIDDLEWARE] Token no encontrado o formato incorrecto")
            return JsonResponse({
                'error': 'Token de autenticación requerido',
                'code': 'AUTHENTICATION_REQUIRED'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        print(f"[MIDDLEWARE] Token extraído: {token[:20]}...")
        
        try:
            # Decodificar token para obtener información del usuario
            decoded_token = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            print(f"[MIDDLEWARE] Token decodificado: {decoded_token}")
            
            user_id = decoded_token.get('user_id')
            es_admin = decoded_token.get('es_admin', False)  # ← Agregar esta línea
            
            if not user_id:
                print(f"[MIDDLEWARE] user_id no encontrado en el token")
                return JsonResponse({
                    'error': 'Token inválido: user_id no encontrado',
                    'code': 'INVALID_TOKEN'
                }, status=401)
            
            print(f"[MIDDLEWARE] user_id extraído: {user_id}")
            
            # Importar aquí para evitar importación circular
            from api.usuario.models.usuario import Usuario
            
            # Obtener usuario de la base de datos
            try:
                usuario = Usuario.objects.get(usuario_id=user_id, es_activo=True)
                print(f"[MIDDLEWARE] Usuario encontrado: {usuario.nombre_usuario}")
            except Usuario.DoesNotExist:
                print(f"[MIDDLEWARE] Usuario no encontrado en BD para user_id: {user_id}")
                return JsonResponse({
                    'error': 'Usuario no encontrado',
                    'code': 'USER_NOT_FOUND'
                }, status=401)
            
            # Agregar información del usuario al request
            request.user_id = user_id
            request.usuario = usuario
            request.es_admin = es_admin  # ← Agregar esta línea
            print(f"[MIDDLEWARE] Información de usuario agregada al request")
            
        except jwt.ExpiredSignatureError:
            print(f"[MIDDLEWARE] Token expirado")
            return JsonResponse({
                'error': 'Token expirado',
                'code': 'TOKEN_EXPIRED'
            }, status=401)
        except jwt.InvalidTokenError as e:
            print(f"[MIDDLEWARE] Token inválido: {e}")
            return JsonResponse({
                'error': 'Token inválido',
                'code': 'INVALID_TOKEN'
            }, status=401)
        except Exception as e:
            print(f"[MIDDLEWARE] Error inesperado: {e}")
            return JsonResponse({
                'error': f'Error de autenticación: {str(e)}',
                'code': 'AUTHENTICATION_ERROR'
            }, status=500)
            
        return None