from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.programa.services.programa_service import ProgramaService
import json
from drf_spectacular.utils import extend_schema

class ProgramaController:
    """Controller para manejar las peticiones HTTP relacionadas con Programa"""
    
    def __init__(self):
        self.service = ProgramaService()

# Instancia global del controller
programa_controller = ProgramaController()

@extend_schema(tags=['Programa - Público'], summary="Listar todos los programas")
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_programas(request):
    """
    Listar todos los programas
    """
    try:
        # Llamar al servicio para obtener programas
        success, response = programa_controller.service.obtener_todos_programas()
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Programa - Público'], summary="Obtener programa por ID")
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_programa(request, programa_id):
    """
    Obtener programa por ID
    """
    try:
        # Llamar al servicio para obtener programa
        success, response = programa_controller.service.obtener_programa_por_id(programa_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Programa - Admin'], summary="Crear nuevo programa")
@api_view(['POST'])
@permission_classes([AllowAny])
def crear_programa(request):
    """
    Crear nuevo programa
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Llamar al servicio para crear programa
        success, response = programa_controller.service.crear_programa(data)
        
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

@extend_schema(tags=['Programa - Admin'], summary="Actualizar programa existente")
@api_view(['PUT'])
@permission_classes([AllowAny])  
def actualizar_programa(request, programa_id):
    """
    Actualizar programa existente
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Llamar al servicio para actualizar programa
        success, response = programa_controller.service.actualizar_programa(programa_id, data)
        
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

@extend_schema(tags=['Programa - Admin'], summary="Eliminar programa")
@api_view(['DELETE'])
@permission_classes([AllowAny])
def eliminar_programa(request, programa_id):
    """
    Eliminar programa
    """
    try:
        # Llamar al servicio para eliminar programa
        success, response = programa_controller.service.eliminar_programa(programa_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Programa - Público'], summary="Listar solo programas activos")
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_programas_activos(request):
    """
    Listar solo programas activos
    """
    try:
        # Llamar al servicio para obtener programas activos
        success, response = programa_controller.service.obtener_programas_activos()
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Programa - Público'], summary="Buscar programas por nombre")
@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_programas(request):
    """
    Buscar programas por nombre
    Query parameter: ?nombre=<nombre_a_buscar>
    """
    try:
        # Obtener parámetro de búsqueda
        nombre = request.GET.get('nombre', '').strip()
        
        if not nombre:
            return Response({
                'error': 'Parámetro "nombre" requerido para la búsqueda'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Llamar al servicio para buscar programas
        success, response = programa_controller.service.buscar_programas_por_nombre(nombre)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Programa - Público'], summary="Endpoint de prueba para verificar conexión de la api")
@api_view(['GET'])
@permission_classes([AllowAny])
def test_programa_connection(request):
    """
    Endpoint de prueba para verificar conexión de la api
    """
    return Response({
        'message': 'API Programa funcionando correctamente',
        'status': 'OK',
        'endpoints': [
            'GET /api/programa/ - Listar todos los programas',
            'GET /api/programa/{id}/ - Obtener programa por ID',
            'POST /api/programa/ - Crear programa',
            'PUT /api/programa/{id}/ - Actualizar programa',
            'DELETE /api/programa/{id}/ - Eliminar programa',
            'GET /api/programa/activos/ - Listar programas activos',
            'GET /api/programa/buscar/?nombre=<nombre> - Buscar programas',
            'GET /api/programa/test/ - Test de conexión'
        ]
    }, status=status.HTTP_200_OK)
