from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.materia.services.materia_service import MateriaService
import json
from drf_spectacular.utils import extend_schema

class MateriaController:
    """Controller para manejar las peticiones HTTP relacionadas con Materia"""
    
    def __init__(self):
        self.service = MateriaService()

# Instancia global del controller
materia_controller = MateriaController()

@extend_schema(tags=['Materia - Público'], summary="Listar todas las materias")
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_materias(request):
    """
    Listar todas las materias
    """
    try:
        # Llamar al servicio para obtener materias
        success, response = materia_controller.service.obtener_todas_materias()
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Público'], summary="Obtener materia por ID")
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_materia(request, materia_id):
    """
    Obtener materia por ID
    """
    try:
        # Llamar al servicio para obtener materia
        success, response = materia_controller.service.obtener_materia_por_id(materia_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Admin'], summary="Crear nueva materia")
@api_view(['POST'])
@permission_classes([AllowAny])  # Cambiar a IsAuthenticated si requiere autenticación
def crear_materia(request):
    """
    Crear nueva materia
    
    Campos requeridos:
    - pensum_id: ID del pensum al que pertenece la materia
    - nombre_materia: Nombre de la materia
    - creditos: Número de créditos (1-10)
    - semestre: Semestre en el que se imparte (1-12)
    
    Campos opcionales:
    - es_obligatoria: True si es obligatoria, False si es electiva (default: True)
    - es_activa: True si está activa, False si está inactiva (default: True)
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Llamar al servicio para crear materia
        success, response = materia_controller.service.crear_materia(data)
        
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

@extend_schema(tags=['Materia - Admin'], summary="Actualizar materia existente")
@api_view(['PUT'])
@permission_classes([AllowAny])  # Cambiar a IsAuthenticated si requiere autenticación
def actualizar_materia(request, materia_id):
    """
    Actualizar materia existente
    
    Todos los campos son opcionales, enviar solo los que se desean actualizar:
    - pensum_id: ID del pensum al que pertenece la materia
    - nombre_materia: Nombre de la materia
    - creditos: Número de créditos (1-10)
    - semestre: Semestre en el que se imparte (1-12)
    - es_obligatoria: True si es obligatoria, False si es electiva
    - es_activa: True si está activa, False si está inactiva
    """
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # Llamar al servicio para actualizar materia
        success, response = materia_controller.service.actualizar_materia(materia_id, data)
        
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

@extend_schema(tags=['Materia - Admin'], summary="Eliminar materia")
@api_view(['DELETE'])
@permission_classes([AllowAny])  # Cambiar a IsAuthenticated si requiere autenticación
def eliminar_materia(request, materia_id):
    """
    Eliminar materia (soft delete - marca es_activa como False)
    """
    try:
        # Llamar al servicio para eliminar materia
        success, response = materia_controller.service.eliminar_materia(materia_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Público'], summary="Listar solo materias activas")
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_materias_activas(request):
    """
    Listar solo materias activas
    """
    try:
        # Llamar al servicio para obtener materias activas
        success, response = materia_controller.service.obtener_materias_activas()
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Público'], summary="Obtener materias por pensum")
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_materias_por_pensum(request, pensum_id):
    """
    Obtener todas las materias de un pensum específico
    """
    try:
        # Llamar al servicio para obtener materias por pensum
        success, response = materia_controller.service.obtener_materias_por_pensum(pensum_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Público'], summary="Obtener materias por semestre")
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_materias_por_semestre(request, semestre):
    """
    Obtener todas las materias de un semestre específico
    """
    try:
        # Llamar al servicio para obtener materias por semestre
        success, response = materia_controller.service.obtener_materias_por_semestre(semestre)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Público'], summary="Buscar materias por nombre")
@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_materias(request):
    """
    Buscar materias por nombre
    Query parameter: ?nombre=<nombre_a_buscar>
    """
    try:
        # Obtener parámetro de búsqueda
        nombre = request.GET.get('nombre', '').strip()
        
        if not nombre:
            return Response({
                'error': 'Parámetro "nombre" requerido para la búsqueda'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Llamar al servicio para buscar materias
        success, response = materia_controller.service.buscar_materias_por_nombre(nombre)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Público'], summary="Listar solo materias obligatorias")
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_materias_obligatorias(request):
    """
    Listar solo materias obligatorias activas
    """
    try:
        # Llamar al servicio para obtener materias obligatorias
        success, response = materia_controller.service.obtener_materias_obligatorias()
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Materia - Público'], summary="Endpoint de prueba para verificar conexión de la api")
@api_view(['GET'])
@permission_classes([AllowAny])
def test_materia_connection(request):
    """
    Endpoint de prueba para verificar conexión de la api
    """
    return Response({
        'message': 'API Materia funcionando correctamente',
        'status': 'OK',
        'endpoints': [
            'GET /api/materia/ - Listar todas las materias',
            'GET /api/materia/{id}/ - Obtener materia por ID',
            'POST /api/materia/ - Crear materia',
            'PUT /api/materia/{id}/ - Actualizar materia',
            'DELETE /api/materia/{id}/ - Eliminar materia',
            'GET /api/materia/activas/ - Listar materias activas',
            'GET /api/materia/pensum/{pensum_id}/ - Obtener materias por pensum',
            'GET /api/materia/semestre/{semestre}/ - Obtener materias por semestre',
            'GET /api/materia/buscar/?nombre=<nombre> - Buscar materias',
            'GET /api/materia/obligatorias/ - Listar materias obligatorias',
            'GET /api/materia/test/ - Test de conexión'
        ]
    }, status=status.HTTP_200_OK)

