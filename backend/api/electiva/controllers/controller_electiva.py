from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.electiva.services.electiva_service import ElectivaService
import json
from drf_spectacular.utils import extend_schema

class ElectivaController:
    """Controller para manejar las peticiones HTTP relacionadas con Electiva"""
    
    def __init__(self):
        self.service = ElectivaService()

# Instancia global del controller
electiva_controller = ElectivaController()

@extend_schema(tags=['Electiva - Público'], summary="Listar todas las electivas")
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_electivas(request):
    """
    Listar todas las electivas
    """
    try:
        # Llamar al servicio para obtener electivas
        success, response = electiva_controller.service.obtener_todas_electivas()
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Electiva - Público'], summary="Obtener electiva por ID")
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_electiva(request, electiva_id):
    """
    Obtener electiva por ID
    """
    try:
        # Llamar al servicio para obtener electiva
        success, response = electiva_controller.service.obtener_electiva_por_id(electiva_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Electiva - Admin'], summary="Crear nueva electiva")
@api_view(['POST'])
@permission_classes([AllowAny])  # Cambiar a IsAuthenticated si requiere autenticación
def crear_electiva(request):
    """
    Crear nueva electiva
    
    Campos requeridos:
    - programa_id: ID del programa al que pertenece la electiva
    - nombre_electiva: Nombre de la electiva
    
    Campos opcionales:
    - es_activa: True si está activa, False si está inactiva (default: True)
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Llamar al servicio para crear electiva
        success, response = electiva_controller.service.crear_electiva(data)
        
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

@extend_schema(tags=['Electiva - Admin'], summary="Actualizar electiva existente")
@api_view(['PUT'])
@permission_classes([AllowAny])  # Cambiar a IsAuthenticated si requiere autenticación
def actualizar_electiva(request, electiva_id):
    """
    Actualizar electiva existente
    
    Todos los campos son opcionales, enviar solo los que se desean actualizar:
    - programa_id: ID del programa al que pertenece la electiva
    - nombre_electiva: Nombre de la electiva
    - es_activa: True si está activa, False si está inactiva
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Llamar al servicio para actualizar electiva
        success, response = electiva_controller.service.actualizar_electiva(electiva_id, data)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
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

@extend_schema(tags=['Electiva - Admin'], summary="Eliminar electiva")
@api_view(['DELETE'])
@permission_classes([AllowAny])  # Cambiar a IsAuthenticated si requiere autenticación
def eliminar_electiva(request, electiva_id):
    """
    Eliminar electiva (soft delete - marca es_activa como False)
    """
    try:
        # Llamar al servicio para eliminar electiva
        success, response = electiva_controller.service.eliminar_electiva(electiva_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Electiva - Público'], summary="Listar solo electivas activas")
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_electivas_activas(request):
    """
    Listar solo electivas activas
    """
    try:
        # Llamar al servicio para obtener electivas activas
        success, response = electiva_controller.service.obtener_electivas_activas()
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Electiva - Público'], summary="Obtener electivas por programa")
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_electivas_por_programa(request, programa_id):
    """
    Obtener todas las electivas de un programa específico
    """
    try:
        # Llamar al servicio para obtener electivas por programa
        success, response = electiva_controller.service.obtener_electivas_por_programa(programa_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Electiva - Público'], summary="Buscar electivas por nombre")
@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_electivas(request):
    """
    Buscar electivas por nombre
    Query parameter: ?nombre=<nombre_a_buscar>
    """
    try:
        # Obtener parámetro de búsqueda
        nombre = request.GET.get('nombre', '').strip()
        
        if not nombre:
            return Response({
                'error': 'Parámetro "nombre" requerido para la búsqueda'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Llamar al servicio para buscar electivas
        success, response = electiva_controller.service.buscar_electivas_por_nombre(nombre)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Electiva - Público'], summary="Endpoint de prueba para verificar conexión de la api")
@api_view(['GET'])
@permission_classes([AllowAny])
def test_electiva_connection(request):
    """
    Endpoint de prueba para verificar conexión de la api
    """
    return Response({
        'message': 'API Electiva funcionando correctamente',
        'status': 'OK',
        'endpoints': [
            'GET /api/electiva/ - Listar todas las electivas',
            'GET /api/electiva/{id}/ - Obtener electiva por ID',
            'POST /api/electiva/crear/ - Crear electiva',
            'PUT /api/electiva/{id}/actualizar/ - Actualizar electiva',
            'DELETE /api/electiva/{id}/eliminar/ - Eliminar electiva',
            'GET /api/electiva/activas/ - Listar electivas activas',
            'GET /api/electiva/programa/{programa_id}/ - Obtener electivas por programa',
            'GET /api/electiva/buscar/?nombre=<nombre> - Buscar electivas',
            'GET /api/electiva/test/ - Test de conexión'
        ]
    }, status=status.HTTP_200_OK)

