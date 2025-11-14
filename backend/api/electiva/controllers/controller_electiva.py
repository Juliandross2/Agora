from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.electiva.services.electiva_service import ElectivaService
from api.electiva.serializers.electiva_serializer import ElectivaCreateSerializer, ElectivaUpdateSerializer
import json
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter

class ElectivaController:
    """Controller para manejar las peticiones HTTP relacionadas con Electiva"""
    
    def __init__(self):
        self.service = ElectivaService()

# Instancia global del controller
electiva_controller = ElectivaController()

@extend_schema(
    tags=['Electiva - Público'],
    summary="Listar todas las electivas",
    description="Devuelve la lista de todas las electivas registradas.",
    responses={
        200: OpenApiResponse(
            description="Lista de electivas (puede estar vacía)",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "message": "Electivas obtenidas exitosamente",
                        "electivas": [
                            {"electiva_id": 1, "programa_id": 1, "nombre_electiva": "Tópicos en IA", "es_activa": True}
                        ],
                        "total": 1
                    }
                ),
                OpenApiExample(
                    "Empty",
                    value={"message": "No hay electivas registradas", "electivas": [], "total": 0}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
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

@extend_schema(
    tags=['Electiva - Público'],
    summary="Obtener electiva por ID",
    parameters=[OpenApiParameter(name='electiva_id', type=int, location=OpenApiParameter.PATH, description='ID de la electiva', required=True)],
    responses={
        200: OpenApiResponse(description="Electiva encontrada", examples=[OpenApiExample("Success", value={"message": "Electiva obtenida exitosamente", "electiva": {"electiva_id": 1, "programa_id": 1, "nombre_electiva": "Tópicos en IA", "es_activa": True}})]),
        404: OpenApiResponse(description="Electiva no encontrada", examples=[OpenApiExample("Not Found", value={"error": "Electiva no encontrada"})]),
        400: OpenApiResponse(description="ID inválido", examples=[OpenApiExample("Invalid ID", value={"error": "ID de electiva inválido"})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
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

@extend_schema(
    tags=['Electiva - Admin'],
    summary="Crear nueva electiva",
    description="Crear una nueva electiva. Campos requeridos: programa_id, nombre_electiva. Opcional: es_activa.",
    request=ElectivaCreateSerializer,
    examples=[
        OpenApiExample("Create", value={"programa_id": 1, "nombre_electiva": "Tópicos en IA", "es_activa": True}),
        OpenApiExample("Minimal", value={"programa_id": 1, "nombre_electiva": "Fundamentos"})
    ],
    responses={
        201: OpenApiResponse(description="Electiva creada exitosamente", examples=[OpenApiExample("Created", value={"message": "Electiva creada exitosamente", "electiva": {"electiva_id": 10, "programa_id": 1, "nombre_electiva": "Fundamentos", "es_activa": True}})]),
        400: OpenApiResponse(description="Datos inválidos o programa no encontrado", examples=[OpenApiExample("Validation", value={"error": "Datos inválidos", "details": {"programa_id": ["El programa especificado no existe"]}})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAuthenticated si aplica
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
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Electiva - Admin'],
    summary="Actualizar electiva existente",
    description="Actualizar una electiva existente. Enviar solo los campos a modificar.",
    parameters=[OpenApiParameter(name='electiva_id', type=int, location=OpenApiParameter.PATH, description='ID de la electiva', required=True)],
    request=ElectivaUpdateSerializer,
    examples=[OpenApiExample("Update", value={"nombre_electiva": "Tópicos Avanzados en IA", "es_activa": False})],
    responses={
        200: OpenApiResponse(description="Electiva actualizada exitosamente", examples=[OpenApiExample("Success", value={"message": "Electiva actualizada exitosamente", "electiva": {"electiva_id": 1, "programa_id": 1, "nombre_electiva": "Tópicos Avanzados en IA", "es_activa": False}})]),
        400: OpenApiResponse(description="Datos inválidos", examples=[OpenApiExample("Validation", value={"error": "Datos inválidos", "details": {"nombre_electiva": ["El nombre de la electiva no puede estar vacío"]}})]),
        404: OpenApiResponse(description="Electiva no encontrada", examples=[OpenApiExample("Not Found", value={"error": "Electiva no encontrada"})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['PUT'])
@permission_classes([AllowAny])
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
        # service returns appropriate dict with error/details
        return Response(response, status=status.HTTP_400_BAD_REQUEST if 'error' in response or 'details' in response else status.HTTP_200_OK)
    except json.JSONDecodeError:
        return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Electiva - Admin'],
    summary="Eliminar electiva (soft delete)",
    description="Marca una electiva como inactiva (es_activa = False).",
    parameters=[OpenApiParameter(name='electiva_id', type=int, location=OpenApiParameter.PATH, description='ID de la electiva', required=True)],
    responses={
        200: OpenApiResponse(description="Electiva marcada como inactiva", examples=[OpenApiExample("Success", value={"message": "Electiva marcada como inactiva"})]),
        404: OpenApiResponse(description="Electiva no encontrada", examples=[OpenApiExample("Not Found", value={"error": "Electiva no encontrada"})]),
        400: OpenApiResponse(description="ID inválido", examples=[OpenApiExample("Invalid", value={"error": "ID de electiva inválido"})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def eliminar_electiva(request, electiva_id):
    """
    Eliminar electiva (soft delete - marca es_activa como False)
    """
    try:
        # Llamar al servicio para eliminar electiva
        success, response = electiva_controller.service.eliminar_electiva(electiva_id)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Electiva - Público'],
    summary="Listar solo electivas activas",
    description="Devuelve electivas con es_activa = True.",
    responses={
        200: OpenApiResponse(description="Electivas activas", examples=[OpenApiExample("Success", value={"message": "Electivas activas obtenidas exitosamente", "electivas": [], "total": 0})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
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
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Electiva - Público'],
    summary="Obtener electivas por programa",
    description="Lista electivas filtradas por programa_id.",
    parameters=[OpenApiParameter(name='programa_id', type=int, location=OpenApiParameter.PATH, description='ID del programa', required=True)],
    responses={
        200: OpenApiResponse(description="Electivas por programa", examples=[OpenApiExample("Success", value={"message": "Electivas del programa 1 obtenidas exitosamente", "electivas": [], "total": 0})]),
        400: OpenApiResponse(description="ID inválido", examples=[OpenApiExample("Invalid", value={"error": "ID de programa inválido"})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
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
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Electiva - Público'],
    summary="Buscar electivas por nombre",
    description="Buscar electivas por nombre parcial. Query parameter: ?nombre=<texto>",
    parameters=[OpenApiParameter(name='nombre', type=str, location=OpenApiParameter.QUERY, description='Texto parcial a buscar', required=True)],
    responses={
        200: OpenApiResponse(description="Electivas encontradas", examples=[OpenApiExample("Success", value={"message": "Electivas encontradas para \"IA\"", "electivas": [], "total": 0})]),
        400: OpenApiResponse(description="Parámetro faltante", examples=[OpenApiExample("Missing", value={"error": 'Parámetro "nombre" requerido para la búsqueda'})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
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
            return Response({'error': 'Parámetro "nombre" requerido para la búsqueda'}, status=status.HTTP_400_BAD_REQUEST)

        # Llamar al servicio para buscar electivas
        success, response = electiva_controller.service.buscar_electivas_por_nombre(nombre)
        
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Electiva - Público'], summary="Endpoint de prueba para verificar conexión de la api", responses={200: OpenApiResponse(description="Estado OK", examples=[OpenApiExample("Test", value={"message": "API Electiva funcionando correctamente", "status": "OK"})])})
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
            'POST /api/electiva/ - Crear electiva',
            'PUT /api/electiva/{id}/ - Actualizar electiva',
            'DELETE /api/electiva/{id}/ - Eliminar electiva',
            'GET /api/electiva/activas/ - Listar electivas activas',
            'GET /api/electiva/programa/{programa_id}/ - Obtener electivas por programa',
            'GET /api/electiva/buscar/?nombre=<nombre> - Buscar electivas',
            'GET /api/electiva/test/ - Test de conexión'
        ]
    }, status=status.HTTP_200_OK)

